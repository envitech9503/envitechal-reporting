"""Quality - Decision Rule / Statement of Conformity (forms ETAL-LAB-708-FF-17 and ETAL-LAB-708-FF-20) - 26-10-2026.

Applies to the drinking-water and waste-water test reports only. A statement of conformity is prepared when the
customer asked for measurement uncertainty / statement of conformity on the sample requisition form (Additional
Requirements of Customer). The chemist picks the sample ID; the test results, methods, customer and standard
come from the report, the specification limits from the standard printed on it, and the expanded uncertainty from
the MOU register. Three replicate results are judged with the binary simple-acceptance rule (guard band 0):
Pass within the specification limits, else Fail.

  * Register per laboratory: records grouped by sample; samples awaiting a statement
  * Customer request form (FF-17): the request as received and the laboratory's follow-up
  * Record (FF-20) per parameter: results x3, mean, SD, decision rule, graph, Pass / Fail per result
  * Workflow: draft -> performed (chemist signs) -> reviewed (QC Manager) -> approved (CEO), then locked
  * PDFs: request form, one record, all records of a sample (annex of the test report)
Roles reuse the control-chart assignments (Laboratory Reviewers page), as the MOU module.
"""
from .shared import *  # noqa: F401,F403
import json as _json
import re as _re
from datetime import date as _date, datetime as _dt
from django.utils import timezone as _tz
from django.shortcuts import redirect as _redirect
from django.db.models import Q as _Q
from django.contrib import messages as _msg

from QC.models import SocRequest, SocRecord, MouStudy, ControlChartDeletion
from QC import soc_rules as _R
from QC.views.control_chart import (_CC_LOCS, _CC_OFFICE, _uname, _user_labs, _is_admin, _can_review, _can_approve,
                                    _default_loc, _user_office, _sig_image, _sig_panels, _SIG_MIN, _FOOT_TOP, _SIG_W)
from QC.views.ia_pdf import _pdf, _resp

# form -> (doc no, title, {location: (issue date, issue no, rev no)}) - the numbers printed on each laboratory's own formats
_FORMS = {'soc_request': ('ETAL-LAB-708-FF-17', 'CUSTOMER REQUEST FORM FOR MOU & SOC', {'Karachi': ('03-10-2022', '01', '01'), 'Lahore': ('09-03-2026', '02', '01')}),
          'soc_record': ('ETAL-LAB-708-FF-20', 'STATEMENT OF CONFORMITY RECORD', {'Karachi': ('03-10-2022', '01', '00')}),
          'soc_report_ww': ('ETAL-LAB-708-FF-18', 'LAB TEST REPORT WW - WASTEWATER WITH DECISION RULE', {'Lahore': ('25-03-2025', '02', '01')}),
          'soc_report_dw': ('ETAL-LAB-708-FF-19', 'LAB TEST REPORT DW - DRINKING WATER WITH DECISION RULE', {'Lahore': ('25-03-2025', '02', '01')})}
_ROLES = {'Karachi': ('(Chemist)', '(QC Manager)', '(CEO)'), 'Lahore': ('(Assistant Manager)', '(Lab Manager)', '(CEO)')}
_DENIED = 'This action is reserved to the %s laboratory\'s QC / Lab Manager and the CEO / administrator.'
_REPORT_LABEL = dict(SocRecord.REPORTS)


# ---------------------------------------------------------------- helpers
def _docctrl(form, location, on=None):
    from EnviTechAlApp import doccontrol as DC
    no, title, per = _FORMS[form]
    d0 = per.get(location)
    default = {'doc_no': no, 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]} if d0 else None
    c = DC.doc_control(form, location, on, default=default)
    if not c.get('set') and not d0:                 # not issued for this laboratory yet: no invented issue / revision
        c = dict(c, issue_no='-', rev_no='-')
    return c


class _Loc:
    def __init__(self, location):
        self.location = location


def _can_manage(user, location):
    if not (user and user.is_authenticated):
        return False
    return _can_approve(user, _Loc(location)) or location in _user_labs(user)


def _is_staff_of(user, location):
    """The laboratory's own staff: office on the e-signature profile (no office = not restricted), its manager or the administrator."""
    if not (user and user.is_authenticated and user.is_active):
        return False
    if _can_manage(user, location):
        return True
    labs = _user_labs(user)
    if labs and location not in labs:
        return False
    return _user_office(user) == location          # a user with no office on the e-signature profile is nobody's staff


def _can_view(user, location):
    """No cross-laboratory viewing (owner decision 27-10-2026): the laboratory's own staff, its QC / Lab Manager and the
    CEO / administrator (an administrator assigned to one laboratory sees that laboratory only)."""
    if not (user and user.is_authenticated and user.is_active):
        return False
    return _is_staff_of(user, location) or _can_manage(user, location)


def _own_lab(user):
    """The laboratory a user may see first: the office on the e-signature profile, else the assigned laboratory."""
    off = _user_office(user)
    if off in _CC_LOCS:
        return off
    labs = sorted(_user_labs(user))
    return labs[0] if labs else ''


def _denied_view(request, location):
    own = _own_lab(request.user)
    if not request.user.is_authenticated:
        return _redirect('/login/?next=' + request.get_full_path())
    return HttpResponse('Records of the %s laboratory are visible to its own staff, its QC / Lab Manager and the CEO only.%s'
                        % (location, (' Your laboratory: %s.' % own) if own else ''), status=403)


def _soc_can_review(user, location):
    """Review: the laboratory's own QC / Lab Manager (Laboratory Reviewers page) or the CEO / administrator."""
    if not (user and user.is_authenticated and user.is_active):
        return False
    return location in _user_labs(user) or _can_approve(user, _Loc(location))


def _can_edit(user, rec):
    if not (user and user.is_authenticated) or rec.locked:
        return False
    if _can_manage(user, rec.location):
        return True
    return rec.status == 'draft' and _is_staff_of(user, rec.location)


def _loc_of(request):
    loc = request.GET.get('location') or request.session.get('soc_loc') or _default_loc(request)
    if loc not in _CC_LOCS:
        loc = 'Karachi'
    request.session['soc_loc'] = loc
    return loc


def _pdate(txt):
    s = (txt or '').strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%d.%m.%Y', '%d-%B-%Y', '%d-%b-%Y', '%d %B %Y', '%d %b %Y', '%d-%m-%y', '%d/%m/%y'):
        try:
            return _dt.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def _date_field(txt, label, errors):
    """A typed date: blank -> None; unreadable -> an error (never silently dropped)."""
    if not (txt or '').strip():
        return None
    d = _pdate(txt)
    if d is None:
        errors.append('%s: "%s" is not a date (use dd-mm-yyyy).' % (label, txt.strip()))
    return d


def _num_field(txt, label, errors):
    if not (txt or '').strip():
        return None
    v = _num(txt)
    if v is None:
        errors.append('%s: "%s" is not a number.' % (label, txt.strip()))
    return v


def _results(P, prefix, label, errors):
    """Three replicate results with dates from the form; unreadable entries are reported, not dropped."""
    vals = []
    for j in range(3):
        raw = (P.get('%sv%d' % (prefix, j)) or '').strip()
        dd = _date_field(P.get('%sd%d' % (prefix, j)), '%s result %d date' % (label, j + 1), errors)
        if not raw:
            continue
        v, t = _res(raw)
        if v is None:
            errors.append('%s result %d: "%s" cannot be judged (enter a number, or "<LOQ" such as <0.0080).' % (label, j + 1, raw)); continue
        vals.append(_rd(v, t, dd))
    return vals


def _num(txt):
    s = (txt or '').strip().replace(',', '') if isinstance(txt, str) else txt
    if s in ('', None):
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _res(txt):
    """A typed result: (value, text) - '<0.0080' is kept as written and judged at the LOQ."""
    from QC.soc_rules import parse_result
    if txt is None or (isinstance(txt, str) and not txt.strip()):
        return None, ''
    return parse_result(txt)


def _rd(v, t, dd):
    d = {'date': dd.isoformat() if dd else '', 'value': v}
    if t:
        d['text'] = t
    return d


def _fmt(v, dp=3):
    if v is None:
        return '-'
    s = ('%.' + str(dp) + 'f') % v
    return s.rstrip('0').rstrip('.') if '.' in s else s


def _d(d):
    return d.strftime('%d-%m-%Y') if d else '-'


def _sample_groups(qs):
    """Records grouped by sample ID (newest sample first)."""
    groups, order = {}, []
    for r in qs:
        if r.sample_id not in groups:
            groups[r.sample_id] = {'sample_id': r.sample_id, 'customer': r.customer, 'report_type': r.report_type, 'records': [], 'request': r.request}
            order.append(r.sample_id)
        groups[r.sample_id]['records'].append(r)
    out = []
    for k in order:
        g = groups[k]
        sts = {x.status for x in g['records']}
        g['status'] = 'approved' if sts == {'approved'} else ('draft' if 'draft' in sts else 'performed' if 'performed' in sts else 'reviewed')
        g['overall'] = 'Fail' if any(x.overall == 'Fail' for x in g['records']) else ('Pass' if all(x.overall == 'Pass' for x in g['records']) else '')
        g['n'] = len(g['records'])
        g['report_label'] = _REPORT_LABEL.get(g['report_type'], g['report_type'])
        out.append(g)
    return out


# ---------------------------------------------------------------- register
def soc_list(request):
    loc = _loc_of(request)
    if not _can_view(request.user, loc):
        own = _own_lab(request.user)
        if own and own != loc and _can_view(request.user, own):
            request.session['soc_loc'] = own
            return _redirect('/qc/soc/?location=%s' % own)
        return _denied_view(request, loc)
    show = request.GET.get('show') or 'open'
    show = show if show in ('open', 'approved', 'all', 'pending') else 'open'
    q = (request.GET.get('q') or '').strip()
    qs = SocRecord.objects.filter(location=loc).select_related('request', 'performed_by', 'reviewed_by', 'approved_by')
    if q:
        qs = qs.filter(_Q(sample_id__icontains=q) | _Q(customer__icontains=q) | _Q(parameter__icontains=q))
    if show == 'open':
        qs = qs.exclude(status='approved')
    elif show == 'approved':
        qs = qs.filter(status='approved')
    sids = list(dict.fromkeys(qs.order_by('-id').values_list('sample_id', flat=True)))     # samples matching; status from all their records
    allrecs = SocRecord.objects.filter(location=loc, sample_id__in=sids).select_related('request').order_by('-id')
    groups = sorted(_sample_groups(allrecs), key=lambda g: sids.index(g['sample_id'])) if show != 'pending' else []
    done = set(SocRecord.objects.filter(location=loc).values_list('sample_id', flat=True))
    pending = [s for s in _R.eligible_samples(loc) if s['sample_id'] not in done] if show in ('pending', 'open') else []
    if q:
        pending = [s for s in pending if q.lower() in (s['sample_id'] + ' ' + (s.get('customer') or '')).lower()]
    for s in pending:
        s['report_label'] = _REPORT_LABEL.get(s['report'], '')
    counts = {'open': len(_sample_groups(SocRecord.objects.filter(location=loc).exclude(status='approved').order_by('-id'))),
              'approved': len(_sample_groups(SocRecord.objects.filter(location=loc, status='approved').order_by('-id'))),
              'all': len(set(SocRecord.objects.filter(location=loc).values_list('sample_id', flat=True))), 'pending': len(pending) if show in ('pending', 'open') else None}
    requests_ = SocRequest.objects.filter(location=loc).order_by('-date', '-id')[:200] if show == 'all' else []
    return render(request, 'soc_list.html', {'loc': loc, 'locs': _CC_LOCS, 'show': show, 'q': q, 'groups': groups, 'pending': pending, 'counts': counts,
                                             'requests': requests_, 'can_manage': _can_manage(request.user, loc), 'is_staff': _is_staff_of(request.user, loc),
                                             'can_review': _soc_can_review(request.user, loc), 'can_approve': _can_approve(request.user, _Loc(loc)), 'ctrl': _docctrl('soc_record', loc),
                                             'ctrl_req': _docctrl('soc_request', loc), 'report_label': _REPORT_LABEL})


# ---------------------------------------------------------------- new statement (from the report)
def soc_api_sample(request):
    """?sample_id= -> the report's header and parameters (results, methods, limits, U from the MOU register) as JSON."""
    sid = (request.GET.get('sample_id') or '').strip()
    loc = request.GET.get('location') or _loc_of(request)
    if not _can_view(request.user, loc):
        return JsonResponse({'error': 'Not your laboratory.'}, status=403)
    if not sid:
        return JsonResponse({'error': 'sample_id is required'}, status=400)
    kind, rep = _R.report_for(sid, request.GET.get('report_type') or '', int(request.GET['report_pk']) if (request.GET.get('report_pk') or '').isdigit() else None)
    if not rep:
        return JsonResponse({'error': 'No drinking-water or waste-water report with sample ID %s.' % sid}, status=404)
    other = _other_lab(rep, loc)
    if other:
        return JsonResponse({'error': 'Sample %s belongs to the %s laboratory; its statement is prepared there.' % (sid, other)}, status=403)
    mou, soc, reg = _R.requisition_flags(sid)
    hdr = _R.report_header(kind, rep)
    rows = _with_printed_limits(request, kind, rep, _R.report_parameters(kind, rep, loc))
    req = SocRequest.objects.filter(location=loc, sample_id=sid).first()
    existing = list(SocRecord.objects.filter(location=loc, sample_id=sid).values_list('parameter', flat=True))
    _cd = _pdate(hdr.get('collection_date')); hdr['collection_dmy'] = _cd.strftime('%d-%m-%Y') if _cd else ''
    return JsonResponse({'sample_id': sid, 'report_type': kind, 'report_label': _REPORT_LABEL.get(kind, kind), 'report_pk': rep.pk, 'header': hdr,
                         'requisition': {'found': bool(reg), 'mou': mou, 'soc': soc, 'mou_text': (reg.inp109 if reg else '') or '', 'soc_text': (reg.inp112 if reg else '') or ''},
                         'request_form': {'id': req.pk, 'decision': req.decision} if req else None, 'existing': existing, 'parameters': rows})


def _other_lab(rep, loc):
    """The other laboratory a report belongs to ('' when it is this laboratory's, or not recorded)."""
    c = (getattr(rep, 'city_location', '') or '').strip().lower()
    for l in _CC_LOCS:
        if c == l.lower() and l != loc:
            return l
    return ''


def _with_printed_limits(request, kind, rep, rows):
    """Limits as the normal test report prints them (its own standard: SEQS / PEQS / NEQS / custom limits)."""
    from QC.soc_report import printed_rows, _matches
    printed = printed_rows(request, kind, rep)
    used = set()
    for r in rows:
        for i, pr in enumerate(printed):
            if i not in used and _matches(pr['desc'], r['parameter']):
                used.add(i)
                lim = (pr.get('limit') or '').strip()
                lo, hi = _R.parse_limit(lim)
                if lim:
                    r['limit'] = lim
                    r['lower'], r['upper'] = lo, hi
                break
    return rows


def soc_new(request):
    user = request.user
    if not (user.is_authenticated and user.is_active):
        return _redirect('/login/')
    loc = _loc_of(request)
    if not _is_staff_of(user, loc):
        own = _user_office(user)
        if own in _CC_LOCS and own != loc and _is_staff_of(user, own):     # remembered choice of the other laboratory: back to the user's own
            return _redirect('/qc/soc/new/?location=%s' % own)
        return HttpResponse('Statements of conformity of the %s laboratory are prepared by its own staff.' % loc, status=403)
    if request.method == 'POST':
        P = request.POST
        sid = (P.get('sample_id') or '').strip()[:60]
        if not sid:
            _msg.error(request, 'Choose the sample ID (or type it) and load its report before creating records.')
            return _redirect('/qc/soc/new/?location=%s' % loc)
        kind, rep = _R.report_for(sid, P.get('report_type') or '', int(P['report_pk']) if (P.get('report_pk') or '').isdigit() else None)
        if rep and (rep.sample_id or '').strip() != sid:                  # the loaded report must be this sample's
            kind, rep = _R.report_for(sid)
        if not rep:
            _msg.error(request, 'No drinking-water or waste-water report with sample ID %s.' % sid)
            return _redirect('/qc/soc/new/?location=%s' % loc)
        other = _other_lab(rep, loc)
        if other:
            _msg.error(request, 'Sample %s belongs to the %s laboratory; its statement is prepared there.' % (sid, other))
            return _redirect('/qc/soc/new/?location=%s' % loc)
        hdr = _R.report_header(kind, rep)
        req = SocRequest.objects.filter(location=loc, sample_id=sid).first()
        idx = sorted({int(m.group(1)) for k in P for m in [_re.match(r'^p(\d+)_on$', k)] if m})
        made, errors = [], []
        for i in idx:
            par = (P.get('p%d_parameter' % i) or '').strip()[:80]
            if not par:
                continue
            from QC.soc_report import _matches as _pm
            dup = next((x for x in SocRecord.objects.filter(location=loc, sample_id=sid) if x.parameter.lower() == par.lower() or _pm(par, x.parameter) or _pm(x.parameter, par)), None)
            if dup:
                errors.append('%s: a record for this parameter and sample exists already (%s).' % (par, dup.parameter)); continue
            if not _R.is_accredited(par, _R.ACCREDITED.get((loc, kind))):
                errors.append('%s: not in the %s laboratory\'s accreditation scope - a statement of conformity applies to accredited parameters only.' % (par, loc)); continue
            perr = []
            vals = _results(P, 'p%d_' % i, par, perr)
            if not vals and not perr:
                perr.append('%s: enter at least one result.' % par)
            lim = (P.get('p%d_limit' % i) or '').strip()[:40]
            lo, hi = _num_field(P.get('p%d_lower' % i), par + ' lower specification', perr), _num_field(P.get('p%d_upper' % i), par + ' upper specification', perr)
            if lo is None and hi is None:
                lo, hi = _R.parse_limit(lim)
            if lo is None and hi is None:
                perr.append('%s: enter the specification limit (upper and / or lower).' % par)
            if lo is not None and hi is not None and lo > hi:
                perr.append('%s: the lower specification is above the upper.' % par)
            uval = _num_field(P.get('p%d_u' % i), par + ' uncertainty', perr)
            if perr:
                errors.extend(perr); continue
            lim = _R.limit_text(lim, lo, hi)
            sidm = P.get('p%d_mou' % i)
            study = MouStudy.objects.filter(pk=int(sidm)).first() if (sidm or '').isdigit() else None
            usrc = (P.get('p%d_usrc' % i) or '').strip()[:200]
            if study is not None:
                su, _lbl, _sid = _R.mou_u(loc, _R.aliases_for(par), vals[0]['value'] if vals else None)
                if uval is None or su is None or abs(uval - su) > 1e-9:          # U typed over the register's value
                    study = None
                    usrc = 'typed by the analyst' + ((' (MOU register gives %s)' % _fmt(su, 4)) if su is not None else '')
            rec = SocRecord(location=loc, request=req, report_type=kind, report_pk=rep.pk, sample_id=sid, customer=hdr['customer'][:200], parameter=par,
                            method=(P.get('p%d_method' % i) or '').strip()[:120], unit=(P.get('p%d_unit' % i) or '').strip()[:20],
                            standard=(P.get('standard') or hdr['standard'] or 'Sindh Environmental Quality Standard 2016')[:120],
                            limit_text=lim, lower=lo, upper=hi, uncertainty=uval, u_source=usrc,
                            mou_study=study, results=vals,
                            created_by=user, legacy={'report_result': (P.get('p%d_result' % i) or '').strip()[:40]})
            rec.save(); made.append(rec)
        for e in errors:
            _msg.error(request, e)
        if made:
            _msg.success(request, '%d statement-of-conformity record%s created for sample %s as draft%s. Check the figures, then sign each record as performed.'
                         % (len(made), '' if len(made) == 1 else 's', sid, '' if len(made) == 1 else 's'), extra_tags=('' if errors else 'ccsaved:soc_new_%s' % loc))
            if not errors:
                return _redirect('/qc/soc/?location=%s&q=%s' % (loc, sid))
        return _redirect('/qc/soc/new/?location=%s&sample=%s' % (loc, sid))
    done = set(SocRecord.objects.filter(location=loc).values_list('sample_id', flat=True))
    samples = _R.eligible_samples(loc)
    return render(request, 'soc_new.html', {'loc': loc, 'locs': _CC_LOCS, 'samples': samples, 'done': done, 'preset': (request.GET.get('sample') or '').strip(),
                                            'today': _date.today().strftime('%d-%m-%Y'), 'rule': SocRecord.RULE, 'ctrl': _docctrl('soc_record', loc)})


# ---------------------------------------------------------------- record
def _rec_ctx(rec):
    rows = []
    for i, r in enumerate(rec.results or []):
        v = r.get('value')
        dd = _pdate(r.get('date'))
        rows.append({'n': i + 1, 'date': _d(dd) if dd else (r.get('date') or ''), 'value': rec.result_text(r), 'verdict': rec.verdict(v)})
    return rows


def soc_detail(request, pk):
    rec = get_object_or_404(SocRecord.objects.select_related('request', 'performed_by', 'reviewed_by', 'approved_by', 'created_by', 'mou_study'), pk=pk)
    user = request.user
    if not _can_view(user, rec.location):
        return _denied_view(request, rec.location)
    siblings = SocRecord.objects.filter(location=rec.location, sample_id=rec.sample_id).exclude(pk=rec.pk).order_by('id')
    return render(request, 'soc_detail.html', {
        'r': rec, 'rows': _rec_ctx(rec), 'siblings': siblings, 'svg': _chart_svg(rec), 'mean': rec.mean_text, 'sd': rec.sd_text,
        'can_edit': _can_edit(user, rec), 'can_perform': rec.status == 'draft' and _is_staff_of(user, rec.location) and bool(rec.values),
        'can_review': rec.status == 'performed' and _soc_can_review(user, rec.location) and rec.performed_by_id != user.id,
        'can_approve': rec.status == 'reviewed' and _can_approve(user, _Loc(rec.location)) and user.id not in (rec.performed_by_id, rec.reviewed_by_id),
        'can_return': rec.status in ('performed', 'reviewed') and _can_manage(user, rec.location),
        'can_unapprove': rec.status == 'approved' and _can_approve(user, _Loc(rec.location)), 'can_delete': _can_manage(user, rec.location) and rec.status != 'approved',
        'ctrl': _docctrl('soc_record', rec.location, rec.created_at.date() if rec.created_at else None), 'report_label': _REPORT_LABEL.get(rec.report_type, rec.report_type),
        'report_url': _report_url(rec)})


def _report_url(rec):
    if not rec.report_pk:
        return ''
    return ('/drinkingwaterReport-pdf/%d/' if rec.report_type == 'dw' else '/wasteWater2Report-pdfReport/%d/') % rec.report_pk


def soc_edit(request, pk):
    rec = get_object_or_404(SocRecord, pk=pk)
    user = request.user
    if not _can_edit(user, rec):
        return HttpResponse('This record is %s and can no longer be edited%s.' % (rec.get_status_display().lower(), '' if rec.locked else ' by you'), status=403)
    errors = []
    if request.method == 'POST':
        P = request.POST
        rec.parameter = (P.get('parameter') or '').strip()[:80] or rec.parameter
        rec.method = (P.get('method') or '').strip()[:120]
        rec.unit = (P.get('unit') or '').strip()[:20]
        rec.standard = (P.get('standard') or '').strip()[:120] or rec.standard
        rec.limit_text = (P.get('limit_text') or '').strip()[:40]
        rec.lower, rec.upper = _num_field(P.get('lower'), 'Lower specification', errors), _num_field(P.get('upper'), 'Upper specification', errors)
        if rec.lower is None and rec.upper is None:
            rec.lower, rec.upper = _R.parse_limit(rec.limit_text)
        if rec.lower is None and rec.upper is None:
            errors.append('Enter the specification limit (upper and / or lower).')
        elif rec.lower is not None and rec.upper is not None and rec.lower > rec.upper:
            errors.append('The lower specification is above the upper.')
        rec.limit_text = _R.limit_text(rec.limit_text, rec.lower, rec.upper)
        rec.uncertainty = _num_field(P.get('uncertainty'), 'Expanded uncertainty', errors)
        rec.u_source = (P.get('u_source') or '').strip()[:200]
        rec.decision_rule = (P.get('decision_rule') or '').strip()[:200] or SocRecord.RULE
        rec.remarks = (P.get('remarks') or '').strip()[:2000]
        vals = _results(P, '', 'Record', errors)
        if not vals and not any('result' in e for e in errors):
            errors.append('Enter at least one result.')
        rec.results = vals
        if not errors:
            if rec.status in ('performed', 'reviewed'):          # changed after a signature: the signatures are cleared, back to draft
                rec.status, rec.performed_by, rec.performed_at, rec.reviewed_by, rec.reviewed_at = 'draft', None, None, None, None
                _msg.warning(request, 'The record was changed after it was signed: the signatures are cleared and it must be signed again.')
            rec.save()
            _msg.success(request, 'Record saved.', extra_tags='ccsaved:soc_edit_%d' % rec.pk)
            return _redirect('soc_detail', rec.pk)
    vals = [{'value': x.get('text') or x.get('value'), 'date': (_d(_pdate(x.get('date'))) if _pdate(x.get('date')) else x.get('date', ''))} for x in (rec.results or [])] + [{}] * 3
    return render(request, 'soc_edit.html', {'r': rec, 'vals': vals[:3], 'errors': errors, 'ctrl': _docctrl('soc_record', rec.location)})


def _apply_action(user, rec, act, reason=''):
    now = _tz.now()
    if act == 'perform':
        if rec.status != 'draft':
            return 'skip', 'Already signed as performed.'
        if not _is_staff_of(user, rec.location):
            return 'forbidden', 'Performed-by signing is reserved to the %s laboratory\'s own staff.' % rec.location
        if not rec.values:
            return 'error', 'Enter the results first.'
        if rec.lower is None and rec.upper is None:
            return 'error', 'Enter the specification limit first.'
        if rec.uncertainty is None:
            return 'error', 'Enter the expanded uncertainty first (it is printed with the statement).'
        rec.status, rec.performed_by, rec.performed_at = 'performed', user, now
        rec.save()
        return 'ok', 'Signed as performed by you. The record now awaits the QC Manager\'s review.'
    if act == 'review':
        if rec.status != 'performed':
            return 'skip', 'Not awaiting review.'
        if not _soc_can_review(user, rec.location):
            return 'forbidden', _DENIED % rec.location
        if rec.performed_by_id == user.id:
            return 'error', 'The person who performed the record cannot also review it.'

        rec.status, rec.reviewed_by, rec.reviewed_at = 'reviewed', user, now
        rec.save()
        return 'ok', 'Reviewed and signed. The record now awaits the CEO\'s approval.'
    if act == 'approve':
        if rec.status != 'reviewed':
            return 'skip', 'Not awaiting approval.'
        if not _can_approve(user, _Loc(rec.location)):
            return 'forbidden', 'Approval is reserved to the CEO / administrator.'
        if user.id in (rec.performed_by_id, rec.reviewed_by_id):
            return 'error', 'The person who performed or reviewed the record cannot also approve it.'

        rec.status, rec.approved_by, rec.approved_at = 'approved', user, now
        rec.save()
        return 'ok', 'Approved and locked.'
    if act == 'return':
        if rec.status not in ('performed', 'reviewed') or not _can_manage(user, rec.location):
            return 'forbidden', _DENIED % rec.location
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason (at least 5 characters).'
        rec.status, rec.performed_by, rec.performed_at, rec.reviewed_by, rec.reviewed_at = 'draft', None, None, None, None
        rec.remarks = (rec.remarks + '\n' if rec.remarks else '') + 'Returned to draft %s by %s: %s' % (_d(now.date()), _uname(user), reason.strip()[:500])
        rec.save()
        return 'ok', 'Returned to draft; the reason is kept in the remarks.'
    if act == 'unapprove':
        if rec.status != 'approved' or not _can_approve(user, _Loc(rec.location)):
            return 'forbidden', 'Only the CEO / administrator can unapprove a record.'
        if len((reason or '').strip()) < 5:
            return 'error', 'Give the reason (at least 5 characters).'
        rec.status, rec.approved_by, rec.approved_at = 'reviewed', None, None
        rec.remarks = (rec.remarks + '\n' if rec.remarks else '') + 'Unapproved %s by %s: %s' % (_d(now.date()), _uname(user), reason.strip()[:500])
        rec.save()
        return 'ok', 'Unapproved; the record is back at the reviewed stage.'
    return 'error', 'Unknown action.'


def soc_action(request, pk):
    if request.method != 'POST':
        return _redirect('soc_detail', pk)
    rec = get_object_or_404(SocRecord, pk=pk)
    st, text = _apply_action(request.user, rec, request.POST.get('action'), request.POST.get('reason') or '')
    if st == 'forbidden':
        return HttpResponse(text, status=403)
    (_msg.success if st == 'ok' else _msg.error)(request, text)
    return _redirect('soc_detail', pk)


def soc_sample_action(request, sample_id):
    """One action on every record of a sample (sign all as performed / review all / approve all)."""
    loc = _loc_of(request)
    if request.method != 'POST':
        return _redirect('/qc/soc/?location=%s&q=%s' % (loc, sample_id))
    done, skipped, problems = 0, 0, []
    for rec in SocRecord.objects.filter(location=loc, sample_id=sample_id).order_by('id'):
        st, text = _apply_action(request.user, rec, request.POST.get('action'), request.POST.get('reason') or '')
        if st == 'ok':
            done += 1
        elif st == 'skip':
            skipped += 1
        else:
            problems.append('%s: %s' % (rec.parameter, text))
    if done:
        _msg.success(request, '%d record%s of sample %s: done.' % (done, '' if done == 1 else 's', sample_id))
    elif not problems:
        _msg.info(request, 'Nothing to do: no record of sample %s is at that stage.' % sample_id)
    for p in problems[:6]:
        _msg.error(request, p)
    return _redirect('/qc/soc/?location=%s&q=%s' % (loc, sample_id))


def soc_delete(request, pk):
    if request.method != 'POST':
        return _redirect('soc_detail', pk)
    rec = get_object_or_404(SocRecord, pk=pk)
    if not _can_manage(request.user, rec.location):
        return HttpResponse(_DENIED % rec.location, status=403)
    if rec.status == 'approved':
        _msg.error(request, 'An approved record is locked: the CEO unapproves it (with the reason) before it can be deleted.')
        return _redirect('soc_detail', pk)
    reason = (request.POST.get('reason') or '').strip()
    if len(reason) < 5:
        _msg.error(request, 'Nothing was deleted: a reason (at least 5 characters) is required.')
        return _redirect('soc_detail', pk)
    snap = {f.name: (getattr(rec, f.attname).isoformat() if hasattr(getattr(rec, f.attname), 'isoformat') else getattr(rec, f.attname)) for f in rec._meta.concrete_fields}
    ControlChartDeletion.objects.create(kind='soc', chart_ref=rec.pk, location=rec.location, activity='SOC', label='%s - %s (%s)' % (rec.sample_id, rec.parameter, rec.customer)[:300],
                                        reason=reason, snapshot=snap, deleted_by=request.user)
    sid = rec.sample_id; loc = rec.location
    rec.delete()
    _msg.success(request, 'Record deleted; a copy is kept in the deletion log.')
    return _redirect('/qc/soc/?location=%s&q=%s&show=all' % (loc, sid))


def soc_deletions(request):
    loc = _loc_of(request)
    if not _can_manage(request.user, loc):
        return HttpResponse(_DENIED % loc, status=403)
    rows = ControlChartDeletion.objects.filter(kind='soc', location=loc).select_related('deleted_by').order_by('-id')[:300]
    return render(request, 'soc_deletions.html', {'rows': rows, 'loc': loc, 'locs': _CC_LOCS})


# ---------------------------------------------------------------- customer request form (FF-17)
def soc_request_edit(request, pk=None):
    user = request.user
    if not (user.is_authenticated and user.is_active):
        return _redirect('/login/')
    req = get_object_or_404(SocRequest, pk=pk) if pk else None
    loc = req.location if req else _loc_of(request)
    if not _is_staff_of(user, loc):
        own = _user_office(user)
        if not req and own in _CC_LOCS and own != loc and _is_staff_of(user, own):
            return _redirect('/qc/soc/request/new/?location=%s%s' % (own, ('&sample=' + request.GET['sample']) if request.GET.get('sample') else ''))
        return HttpResponse('Requests of the %s laboratory are entered by its own staff.' % loc, status=403)
    if req and req.locked:
        return HttpResponse('This request form is authorised and locked. The QC / Lab Manager or the CEO clears the authorisation first ("Unlock").', status=403)
    manager = _can_manage(user, loc)
    if request.method == 'POST':
        P = request.POST
        obj = req or SocRequest(location=loc, created_by=user)
        errors = []
        obj.sample_id = (P.get('sample_id') or '').strip()[:60]
        if not obj.sample_id:
            errors.append('Sample ID is required.')
        elif SocRequest.objects.filter(location=loc, sample_id=obj.sample_id).exclude(pk=obj.pk).exists():
            errors.append('A request form for sample %s exists already.' % obj.sample_id)
        else:
            kind, rep = _R.report_for(obj.sample_id)
            other = _other_lab(rep, loc) if rep else ''
            if other:
                errors.append('Sample %s belongs to the %s laboratory; its request form is kept there.' % (obj.sample_id, other))
        obj.date = _date_field(P.get('date'), 'Date', errors)
        for f in ('reason', 'organization', 'customer_name', 'contact', 'address', 'analysis_other', 'parameters', 'req_other', 'reporting', 'customer_sign_name'):
            setattr(obj, f, (P.get(f) or '').strip()[:obj._meta.get_field(f).max_length or 4000])
        obj.analysis = P.get('analysis') if P.get('analysis') in dict(SocRequest.ANALYSES) else 'ww'
        for f in ('req_mou', 'req_soc', 'req_opinion', 'req_limits'):
            setattr(obj, f, P.get(f) == '1')
        if manager:                                   # the follow-up action is the laboratory's (QC / Lab Manager, CEO)
            obj.decision = P.get('decision') if P.get('decision') in ('approved', 'denied', '') else ''
            obj.decision_comment = (P.get('decision_comment') or '').strip()[:obj._meta.get_field('decision_comment').max_length or 4000]
            obj.decision_date = _date_field(P.get('decision_date'), 'Follow-up date', errors)
        if errors:
            for e in errors:
                _msg.error(request, e)
            return render(request, 'soc_request_edit.html', {'f': obj, 'loc': loc, 'analyses': SocRequest.ANALYSES, 'ctrl': _docctrl('soc_request', loc), 'manager': manager})
        obj.save()
        SocRecord.objects.filter(location=loc, sample_id=obj.sample_id, request__isnull=True).update(request=obj)
        _msg.success(request, 'Request form saved.', extra_tags='ccsaved:soc_req_%s' % (pk or 'new'))
        return _redirect('soc_request_detail', obj.pk)
    f = req or SocRequest(location=loc, sample_id=(request.GET.get('sample') or '').strip(), date=_date.today())
    if not req and f.sample_id:                                     # prefill from the report / requisition
        kind, rep = _R.report_for(f.sample_id)
        if rep:
            h = _R.report_header(kind, rep)
            f.organization, f.customer_name, f.address = h['customer'][:200], h['attention'][:150], h['address'][:300]
            f.analysis = 'dw' if kind == 'dw' else 'ww'
            f.parameters = ', '.join(p['parameter'] for p in _R.report_parameters(kind, rep, loc))[:4000]
            f.reason = 'To ensure the %s sample parameters results are within limits according to %s' % ('drinking water' if kind == 'dw' else 'wastewater', h['standard'] or 'SEQS-2016')
        mou, soc, reg = _R.requisition_flags(f.sample_id)
        f.req_mou, f.req_soc = mou or not reg, soc or not reg
    return render(request, 'soc_request_edit.html', {'f': f, 'loc': loc, 'analyses': SocRequest.ANALYSES, 'ctrl': _docctrl('soc_request', loc), 'manager': manager})


def soc_request_detail(request, pk):
    req = get_object_or_404(SocRequest.objects.select_related('authorised_by', 'created_by'), pk=pk)
    user = request.user
    if not _can_view(user, req.location):
        return _denied_view(request, req.location)
    return render(request, 'soc_request_detail.html', {'q': req, 'records': req.records.order_by('id'), 'can_edit': _is_staff_of(user, req.location) and not req.locked,
                                                       'can_authorise': not req.locked and _can_manage(user, req.location), 'can_unlock': req.locked and _can_manage(user, req.location),
                                                       'ctrl': _docctrl('soc_request', req.location, req.date)})


def soc_request_action(request, pk):
    req = get_object_or_404(SocRequest, pk=pk)
    if request.method != 'POST':
        return _redirect('soc_request_detail', pk)
    act = request.POST.get('action')
    if not _can_manage(request.user, req.location):
        return HttpResponse(_DENIED % req.location, status=403)
    if act in ('authorise', 'deny'):
        if req.locked:
            _msg.error(request, 'The form is authorised already.'); return _redirect('soc_request_detail', pk)
        if act == 'deny':
            note = (request.POST.get('comment') or '').strip()
            if len(note) < 5:
                _msg.error(request, 'Give the comment for denying the request (at least 5 characters).'); return _redirect('soc_request_detail', pk)
            req.decision, req.decision_comment = 'denied', note[:2000]
        else:
            if req.decision == 'denied':                 # a denial comment does not stay under "Request Approved"
                req.decision_comment = (request.POST.get('comment') or '').strip()[:2000]
            req.decision = 'approved'
        req.authorised_by, req.authorised_at = request.user, _tz.now()
        req.decision_date = req.decision_date or _date.today()
        req.save(); _msg.success(request, 'Request %s; the form is authorised and signed by you.' % ('denied' if req.decision == 'denied' else 'approved'))
    elif act == 'unlock':
        req.authorised_by = req.authorised_at = None
        req.save(); _msg.success(request, 'Authorisation cleared; the form can be edited and must be authorised again.')
    return _redirect('soc_request_detail', pk)


# ---------------------------------------------------------------- document control, manual
def soc_doccontrol(request):
    from EnviTechAlApp.doccontrol import revision_on
    user = request.user
    labs = set(_CC_LOCS) if (_is_admin(user) and not _user_labs(user)) else (_user_labs(user) if user.is_authenticated else set())
    if not labs:
        return HttpResponse('The form numbers are kept by the laboratory\'s QC / Lab Manager and the administrator.', status=403)
    if request.method == 'POST':
        P = request.POST
        form, loc = P.get('form'), P.get('location')
        if form in _FORMS and loc in _CC_LOCS and loc not in labs:
            return HttpResponse('You keep the form numbers of the %s laboratory only.' % ', '.join(sorted(labs)), status=403)
        if form in _FORMS and loc in _CC_LOCS:
            from EnviTechAlApp.models import InventoryDocControl
            obj, _ = InventoryDocControl.objects.get_or_create(module=form, location=loc)
            clean = lambda v, n: '' if (v or '').strip() in ('-', 'TBA') else (v or '').strip()[:n]
            obj.doc_no, obj.issue_date, obj.issue_no, obj.rev_no = clean(P.get('doc_no'), 60), clean(P.get('issue_date'), 20), clean(P.get('issue_no'), 10), clean(P.get('rev_no'), 10)
            try:
                obj.updated_by = request.user
            except Exception:
                pass
            obj.save()
            _msg.success(request, 'Saved. Use the Document Control register for revision history.')
        return _redirect('soc_doccontrol')
    grid = []
    for form, (no, title, per) in _FORMS.items():
        for loc in _CC_LOCS:
            if loc not in labs:
                continue
            c = _docctrl(form, loc)
            grid.append({'form': form, 'title': title, 'location': loc, 'ctrl': c})
    return render(request, 'soc_doccontrol.html', {'grid': grid})


def soc_manual(request):
    return render(request, 'soc_manual.html', {})


# ---------------------------------------------------------------- chart (SVG for the page)
def _u_ends(rec, vals):
    """Ends of the uncertainty bars to fit on the chart (a lower end below zero is not drawn for a one-sided limit)."""
    u = rec.uncertainty or 0
    if not u:
        return []
    out = [v + u for v in vals if isinstance(v, (int, float))]
    out += [v - u for v in vals if isinstance(v, (int, float)) and (v - u >= 0 or rec.lower is not None)]
    return out


def _chart_svg(rec):
    vals = [r.get('value') for r in (rec.results or [])]
    pts = [v for v in vals if isinstance(v, (int, float))]
    if not pts:
        return ''
    cand = pts + [x for x in (rec.upper, rec.lower) if x is not None] + _u_ends(rec, pts)
    lo, hi = min(cand), max(cand)
    span = (hi - lo) or (abs(hi) or 1.0)
    lo, hi = lo - span * 0.25, hi + span * 0.25
    if rec.lower is None and min(cand) >= 0:          # one-sided limit, non-negative results: the axis starts at zero
        lo = 0.0
    W, H, L, T, R, B = 640, 260, 60, 20, 20, 40
    def y(v):
        return T + (H - T - B) * (hi - v) / (hi - lo)
    n = len(vals)
    xs = [L + (W - L - R) * (i + 0.5) / n for i in range(n)]
    out = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" style="font-family:Calibri,Arial;font-size:11px">' % (W, H)]
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" stroke="#cbd5e1"/>' % (L, T, W - L - R, H - T - B))
    for k in range(6):
        v = lo + (hi - lo) * k / 5
        out.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#eef2f6"/><text x="%d" y="%.1f" text-anchor="end" fill="#64748b">%s</text>' % (L, W - R, y(v), y(v), L - 6, y(v) + 4, _fmt(v, 3)))
    for lim, lbl, col in ((rec.upper, 'Upper specification', '#dc2626'), (rec.lower, 'Lower specification', '#2563eb')):
        if lim is not None:
            out.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/><text x="%d" y="%.1f" fill="%s">%s %s</text>' % (L, W - R, y(lim), y(lim), col, L + 6, y(lim) - 5, col, lbl, _fmt(lim)))
    for i, (x, v) in enumerate(zip(xs, vals)):
        if not isinstance(v, (int, float)):
            continue
        u = rec.uncertainty or 0
        if u:
            out.append('<line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" stroke="#16a34a" stroke-width="1"/>' % (x, x, y(min(v + u, hi)), y(max(v - u, lo))))
        ok = rec.verdict(v) == 'Pass'
        out.append('<rect x="%.1f" y="%.1f" width="8" height="8" transform="rotate(45 %.1f %.1f)" fill="%s"/>' % (x - 4, y(v) - 4, x, y(v), '#16a34a' if ok else '#dc2626'))
        out.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#334155">%d</text><text x="%.1f" y="%d" text-anchor="middle" font-weight="700" fill="%s">%s</text>'
                   % (x, H - B + 14, i + 1, x, H - B + 28, '#16a34a' if ok else '#dc2626', rec.verdict(v)))
    out.append('<text x="%d" y="%d" text-anchor="middle" fill="#0f5132" font-weight="700" font-size="12">Graphical Representation of Binary Statement - Simple Acceptance</text>' % ((L + W - R) / 2, 12))
    out.append('</svg>')
    return ''.join(out)


# ---------------------------------------------------------------- PDFs
def _draw_chart(pdf, rec, x0, y0, w, h):
    """The graph of the record on the PDF: results (diamonds), U bars, specification lines."""
    f = pdf.fam
    vals = [r.get('value') for r in (rec.results or []) if isinstance(r.get('value'), (int, float))]
    if not vals:
        return
    cand = vals + [x for x in (rec.upper, rec.lower) if x is not None] + _u_ends(rec, vals)
    lo, hi = min(cand), max(cand)
    span = (hi - lo) or (abs(hi) or 1.0)
    lo, hi = lo - span * 0.25, hi + span * 0.25
    if rec.lower is None and min(cand) >= 0:          # one-sided limit, non-negative results: the axis starts at zero
        lo = 0.0
    L, T, R, B = x0 + 16, y0 + 8, x0 + w - 4, y0 + h - 10
    def y(v):
        return T + (B - T) * (hi - v) / (hi - lo)
    pdf.set_draw_color(120, 120, 120); pdf.rect(x0, y0, w, h)
    pdf.set_font(f, 'B', 7.5); pdf.set_xy(x0, y0 + 1.5); pdf.cell(w, 4, 'Graphical Representation of Binary Statement - Simple Acceptance', 0, 0, 'C')
    pdf.set_draw_color(200, 200, 200); pdf.rect(L, T, R - L, B - T)
    pdf.set_font(f, '', 6)
    for k in range(6):
        v = lo + (hi - lo) * k / 5
        pdf.set_draw_color(235, 238, 242); pdf.line(L, y(v), R, y(v))
        pdf.set_xy(x0 + 1, y(v) - 1.5); pdf.cell(14, 3, _fmt(v, 3), 0, 0, 'R')
    n = len(vals)
    xs = [L + (R - L) * (i + 0.5) / n for i in range(n)]
    for lim, lbl, col in ((rec.upper, 'Upper specification', (220, 38, 38)), (rec.lower, 'Lower specification', (37, 99, 235))):
        if lim is not None:
            pdf.set_draw_color(*col); pdf.set_line_width(0.5); pdf.line(L, y(lim), R, y(lim)); pdf.set_line_width(0.2)
            pdf.set_text_color(*col); pdf.set_xy(L + 2, y(lim) - 3.6); pdf.cell(60, 3, '%s %s' % (lbl, _fmt(lim)), 0, 0, 'L'); pdf.set_text_color(0, 0, 0)
    for i, (x, v) in enumerate(zip(xs, vals)):
        ok = rec.verdict(v) == 'Pass'
        col = (22, 163, 74) if ok else (220, 38, 38)
        u = rec.uncertainty or 0
        if u:
            ut, ub = min(v + u, hi), max(v - u, lo)                     # the bar is kept inside the plot
            pdf.set_draw_color(*col); pdf.line(x, y(ut), x, y(ub))
            if ut == v + u:
                pdf.line(x - 1, y(ut), x + 1, y(ut))
            if ub == v - u:
                pdf.line(x - 1, y(ub), x + 1, y(ub))
        pdf.set_fill_color(*col); pdf.set_draw_color(*col)
        s = 1.4
        try:
            pdf.polygon([(x, y(v) - s), (x + s, y(v)), (x, y(v) + s), (x - s, y(v))], style='F')
        except Exception:
            pdf.rect(x - 1, y(v) - 1, 2, 2, 'F')
        pdf.set_xy(x - 10, B + 0.5); pdf.set_font(f, '', 6.5); pdf.cell(20, 3, 'Result %d' % (i + 1), 0, 0, 'C')
        pdf.set_xy(x - 10, B + 3.8); pdf.set_font(f, 'B', 7); pdf.set_text_color(*col); pdf.cell(20, 3.5, rec.verdict(v), 0, 0, 'C'); pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)


def _panels(pdf, f, items, top, blk_h, LINE, GREY, note='Signed on the paper record'):
    """Signature panels: (label, role, name, image, on_paper). A name signed on the paper record (induction) is printed
    with 'Signed on the paper record' instead of 'Electronically signed'."""
    _sig_panels(pdf, f, [(l, r, (n if not paper else ''), img) for l, r, n, img, paper in items], top, blk_h, LINE, GREY)
    for i, (l, r, n, img, paper) in enumerate(items):
        if paper:
            x = 10 + i * (_SIG_W + 2.0)
            pdf.set_xy(x, top + blk_h / 2 - 6); pdf.set_font(f, '', 6.5); pdf.set_text_color(110, 110, 110)
            pdf.cell(_SIG_W, 4, note, 0, 0, 'C')
            pdf.set_xy(x, top + blk_h / 2 - 2); pdf.set_font(f, 'B', 7.5); pdf.set_text_color(0, 0, 0)
            pdf.cell(_SIG_W, 4, n, 0, 0, 'C')


def _record_page(pdf, rec, ctrl):
    f = pdf.fam
    GREEN, GREY, LINE = (15, 81, 50), (242, 245, 243), (120, 120, 120)
    if pdf.page_no() == 0 or pdf.get_y() > 45:          # _pdf() opens the first page already
        pdf.add_page()
    pdf.set_draw_color(*LINE)
    def kv(items, h=5.6):
        for lbl, val, wl, wv in items:
            pdf.set_font(f, 'B', 7.8); pdf.set_fill_color(*GREY); pdf.cell(wl, h, lbl, 1, 0, 'L', fill=True)
            fs = 8.0; pdf.set_font(f, '', fs); txt = str(val if val not in (None, '') else '-')
            while pdf.get_string_width(txt) > wv - 2 and fs > 6.0:          # smaller type before anything is cut
                fs -= 0.4; pdf.set_font(f, '', fs)
            while pdf.get_string_width(txt) > wv - 2 and len(txt) > 4:
                txt = txt[:-1]
            pdf.cell(wv, h, txt, 1, 0, 'L')
        pdf.ln(h)
    kv([('Name of Customer', rec.customer, 34, 106), ('Sample ID', rec.sample_id, 22, 28)])
    kv([('Parameter', rec.parameter, 34, 56), ('Method', rec.method, 22, 28), ('Unit', rec.unit or '-', 12, 38)])
    kv([('Name of Standard', rec.standard, 34, 106), ('Report', _REPORT_LABEL.get(rec.report_type, rec.report_type), 22, 28)])
    pdf.ln(2)
    cols = [('S. No.', 14), ('Date', 24), ('Results', 26), ('Upper Specification', 32), ('Lower Specification', 32), ('Uncertainty  ±', 26), ('%s Limit' % ('SEQS' if 'Sindh' in rec.standard else 'Spec.'), 36)]
    pdf.set_font(f, 'B', 7.2); pdf.set_fill_color(*GREEN); pdf.set_text_color(255, 255, 255)
    for lbl, w in cols:
        pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
    pdf.ln(6); pdf.set_text_color(0, 0, 0); pdf.set_font(f, '', 7.8)
    for i, r in enumerate(rec.results or []):
        v = r.get('value')
        d = _pdate(r.get('date')) if r.get('date') else None
        vals = [str(i + 1), _d(d) if d else (r.get('date') or ''), rec.result_text(r), _fmt(rec.upper, 4), _fmt(rec.lower, 4), _fmt(rec.uncertainty, 4), rec.spec_text]
        for (lbl, w), t in zip(cols, vals):
            pdf.cell(w, 5.4, t, 1, 0, 'C')
        pdf.ln(5.4)
    pdf.set_fill_color(*GREY); pdf.set_font(f, 'B', 7.8)
    pdf.cell(38, 5.4, 'Mean', 1, 0, 'L', fill=True); pdf.cell(26, 5.4, rec.mean_text, 1, 0, 'C'); pdf.cell(126, 5.4, '', 1, 1)
    pdf.cell(38, 5.4, 'Standard Deviation', 1, 0, 'L', fill=True); pdf.cell(26, 5.4, rec.sd_text, 1, 0, 'C'); pdf.cell(126, 5.4, '', 1, 1)
    pdf.ln(2)
    y0 = pdf.get_y()
    pdf.set_fill_color(230, 238, 246); pdf.rect(10, y0, 190, 27, 'F')
    pdf.set_xy(12, y0 + 1); pdf.set_font(f, 'B', 7.8); pdf.cell(186, 4.5, 'Decision Criteria (By Decision Rule)', 0, 1)
    pdf.set_x(12); pdf.set_font(f, '', 7.6); pdf.multi_cell(186, 4, rec.decision_rule, new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(12); pdf.set_font(f, 'B', 7.6); pdf.cell(186, 4.5, 'Statement of conformity reported as:', 0, 1)
    pdf.set_x(12); pdf.set_font(f, '', 7.4); pdf.cell(186, 3.8, '*Pass - the measured value is within %sthe specification Limit' % ('(below) ' if rec.lower is None else ''), 0, 1)
    pdf.set_x(12); pdf.cell(186, 3.8, '*Fail - the measured value is outside %sthe specification Limit' % ('(above) ' if rec.lower is None else ''), 0, 1)
    pdf.set_y(y0 + 29); yc = pdf.get_y()
    _draw_chart(pdf, rec, 10, yc, 190, 64)
    pdf.set_y(yc + 66)
    pdf.set_font(f, 'B', 8); pdf.cell(40, 6, 'Statement of Conformity:', 0, 0)
    for i, vd in enumerate(rec.verdicts):
        col = (22, 163, 74) if vd == 'Pass' else (220, 38, 38)
        pdf.set_text_color(*col); pdf.cell(28, 6, '%d: %s' % (i + 1, vd), 0, 0, 'C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(f, 'B', 8.5); pdf.cell(0, 6, 'Overall: %s' % (rec.overall or '-'), 0, 1, 'R')
    notes = []
    if rec.uncertainty is not None:
        notes.append('Expanded uncertainty ± %s %s (%s).' % (_fmt(rec.uncertainty, 4), rec.unit, rec.u_source or 'as recorded'))
    if rec.report_pk:
        notes.append('Results of the test report (sample %s); result 1 as reported%s.' % (rec.sample_id, (': %s' % rec.legacy.get('report_result')) if (rec.legacy or {}).get('report_result') else ''))
    if rec.censored:
        notes.append('Results written "<x" are below the limit of quantification (LOQ = x); the decision is taken at the LOQ%s.' % (', and the mean (*) takes them at the LOQ' if len(rec.censored) < len(rec.results or []) else ''))
    if rec.inducted:
        notes.append('%s (%s).' % ('Taken from the issued test report' if rec.legacy.get('sign_note') else 'Inducted from the laboratory record', (rec.legacy.get('file') or '')[:80]))
    if rec.remarks:
        notes.append('Remarks: ' + rec.remarks.replace('\n', ' | '))
    pdf.set_font(f, '', 6.6); pdf.set_text_color(60, 60, 60)
    for n in notes:
        pdf.set_x(10); pdf.multi_cell(190, 3.3, '- ' + n, new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    top = max(pdf.get_y() + 2, _FOOT_TOP - 28)
    if top + _SIG_MIN > _FOOT_TOP + 4:
        pdf.add_page(); top = pdf.get_y() + 3
    pdf.set_auto_page_break(False)
    def who(u, at, name):
        if at and u:
            return _uname(u), _sig_image(u), False
        return name or '', None, bool(name) or rec.inducted
    roles = _ROLES.get(rec.location, _ROLES['Karachi'])
    _panels(pdf, f, [('Performed By', roles[0]) + who(rec.performed_by, rec.performed_at, rec.performed_name),
                     ('Reviewed By', roles[1]) + who(rec.reviewed_by, rec.reviewed_at, rec.reviewed_name),
                     ('Approved By', roles[2]) + who(rec.approved_by, rec.approved_at, rec.approved_name)], top, max(_SIG_MIN, _FOOT_TOP - top), LINE, GREY, note=rec.paper_sign_text)
    pdf.set_auto_page_break(True, 30)


def soc_pdf(request, pk):
    rec = get_object_or_404(SocRecord, pk=pk)
    if not _can_view(request.user, rec.location):
        return _denied_view(request, rec.location)
    ctrl = _docctrl('soc_record', rec.location, rec.created_at.date() if rec.created_at else None)
    wm = '' if rec.status == 'approved' else 'NOT APPROVED'
    pdf = _pdf(_FORMS['soc_record'][1], '%s LABORATORY  -  %s  -  %s' % (rec.location.upper(), rec.sample_id, rec.parameter.upper()), ctrl, rec.location, wm=wm)
    pdf.alias_nb_pages(); pdf.set_auto_page_break(True, 30)
    _record_page(pdf, rec, ctrl)
    return _resp(pdf, 'SOC_%s_%s_%s' % (rec.location, rec.sample_id, rec.parameter))


def soc_sample_pdf(request, sample_id):
    """Lab Test Report with Decision Rule (FF-18 waste water / FF-19 drinking water): the accredited parameters of the
    sample with their uncertainty, the standard's limits and the statement of conformity; signed by the people who
    performed, reviewed and approved the records."""
    loc = _loc_of(request)
    if not _can_view(request.user, loc):
        return _denied_view(request, loc)
    recs = list(SocRecord.objects.filter(location=loc, sample_id=sample_id).select_related('performed_by', 'reviewed_by', 'approved_by').order_by('id'))
    if not recs:
        return HttpResponse('No statement of conformity for sample %s.' % sample_id, status=404)
    r0 = recs[0]
    form = 'soc_report_dw' if r0.report_type == 'dw' else 'soc_report_ww'
    ctrl = _docctrl(form, loc, r0.created_at.date() if r0.created_at else None)
    wm = '' if all(r.status == 'approved' for r in recs) else 'NOT APPROVED'
    kind, rep = _R.report_for(sample_id, r0.report_type, r0.report_pk)
    kind = kind or r0.report_type
    if rep and request.GET.get('format') != 'record':
        # the laboratory's normal test report of the sample, with the uncertainty column and the statement of conformity
        from QC.soc_report import soc_context
        soc = soc_context(recs)
        from QC.soc_report import result_column
        soc['result_col'] = result_column(kind, rep)
        c = ctrl
        dno = c['doc_no'] if c.get('doc_no') not in (None, '', 'TBA') else _FORMS[form][0]
        idate = (c.get('issue_date') or '').strip()
        if _re.match(r'^\d{2}-\d{2}-\d{4}$', idate):
            idate = idate[:6] + idate[8:]                  # dd-mm-yy, as the reports print it
        soc['doc'] = (dno, 'Issue Date: %s' % (idate if idate not in ('', '-') else 'TBA'),
                      'Issue:%s Rev:%s' % (c.get('issue_no') or '-', c.get('rev_no') or '-'))
        if kind == 'dw':
            from EnviTechAlApp.views.generate import generatePDF_report as _gen
        else:
            from EnviTechAlApp.views.waste import wasteWater2Pdf1 as _gen
        buf = _gen(request, rep.pk, return_bytes=True, soc=soc)
        resp = HttpResponse(buf.getvalue(), content_type='application/pdf')
        resp['Content-Disposition'] = 'inline; filename="%s-Decision-Rule.pdf"' % (rep.lab_report_no or sample_id)
        resp['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
    if rep:
        hdr = _R.report_header(kind, rep)
    else:                                   # inducted record without the report in the software: the request form supplies the customer details
        q = r0.request
        d1 = next((r.get('date') for r in (r0.results or []) if r.get('date')), '')
        hdr = {'customer': r0.customer, 'address': (q.address if q else ''), 'attention': (q.customer_name if q else ''), 'lab_report_no': '-',
               'collection_date': _d(_pdate(d1)) if _pdate(d1) else d1, 'analysis': '-', 'description': dict(SocRecord.REPORTS).get(r0.report_type, ''), 'standard': r0.standard}
    std_short = 'PEQS' if 'Punjab' in r0.standard else 'NEQS' if 'National' in r0.standard else 'SEQS'
    pdf = _pdf('LAB TEST REPORT %s WITH DECISION RULE' % ('DW - DRINKING WATER' if kind == 'dw' else 'WW - WASTEWATER'),
               '%s LABORATORY  -  SAMPLE %s' % (loc.upper(), sample_id), ctrl, loc, wm=wm)
    pdf.alias_nb_pages(); pdf.set_auto_page_break(True, 30)
    f = pdf.fam
    GREEN, GREY, LINE = (15, 81, 50), (242, 245, 243), (120, 120, 120)
    pdf.set_draw_color(*LINE)
    def kv(items, h=5.4):
        for lbl, val, wl, wv in items:
            pdf.set_font(f, 'B', 7.8); pdf.set_fill_color(*GREY); pdf.cell(wl, h, lbl, 1, 0, 'L', fill=True)
            fs = 8.0; pdf.set_font(f, '', fs); txt = str(val if val not in (None, '') else '-')
            while pdf.get_string_width(txt) > wv - 2 and fs > 6.0:          # smaller type before anything is cut
                fs -= 0.4; pdf.set_font(f, '', fs)
            while pdf.get_string_width(txt) > wv - 2 and len(txt) > 4:
                txt = txt[:-1]
            pdf.cell(wv, h, txt, 1, 0, 'L')
        pdf.ln(h)
    kv([('Report to', hdr['customer'], 28, 86), ('Lab Report No', hdr['lab_report_no'], 26, 50)])
    kv([('Address', hdr['address'], 28, 86), ('Sample ID', sample_id, 26, 50)])
    kv([('Attention', hdr['attention'], 28, 86), ('Collection date', hdr['collection_date'], 26, 50)])
    kv([('Sample description', hdr['description'], 28, 86), ('Date of analysis', hdr['analysis'], 26, 50)])
    pdf.ln(2)
    pdf.set_font(f, 'B', 9); pdf.cell(190, 6, 'ANALYTICAL TEST REPORT', 1, 1, 'C')
    cols = [('Sr. #', 10), ('Parameters / Analytes Description', 56), ('Methods', 34), ('Unit', 14), ('Test Results', 24), ('Uncertainty ±U', 24), ('%s Limits' % std_short, 28)]
    pdf.set_font(f, 'B', 7.2); pdf.set_fill_color(*GREY)
    for lbl, w in cols:
        pdf.cell(w, 6, lbl, 1, 0, 'C', fill=True)
    pdf.ln(6); pdf.set_font(f, '', 7.8)
    for i, r in enumerate(recs):
        res = (r.legacy or {}).get('report_result') or (r.result_text((r.results or [None])[0]) if r.results else '-')
        vals = [str(i + 1), r.parameter + '***', r.method or '-', r.unit or '-', res, _fmt(r.uncertainty, 4) if r.uncertainty is not None else 'N.A', r.spec_text]
        for (lbl, w), t in zip(cols, vals):
            while pdf.get_string_width(t) > w - 2 and len(t) > 3:
                t = t[:-1]
            pdf.cell(w, 5.4, t, 1, 0, 'C' if lbl != 'Parameters / Analytes Description' else 'L')
        pdf.ln(5.4)
    pdf.ln(1.5); pdf.set_font(f, '', 6.8); pdf.set_text_color(60, 60, 60)
    for n in ['*APHA Standard Methods for Examination of water & wastewater 24th Edition (2023).',
              '*** Implies that this parameter is in our accreditation scope.',
              '%s Limits = %s.' % (std_short, r0.standard),
              'N.D. = Not Detected.    "-" = the parameter is not regulated under the standard.']:
        pdf.set_x(10); pdf.multi_cell(190, 3.4, n, new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0); pdf.ln(2)
    passes = [r.parameter for r in recs if r.overall == 'Pass']
    fails = [r.parameter for r in recs if r.overall == 'Fail']
    pdf.set_font(f, 'B', 8.5); pdf.cell(190, 5, 'Statement of Conformity:', 0, 1)
    pdf.set_font(f, 'B', 8); pdf.cell(190, 4.6, '    -  Result = %s' % ('Pass' if passes and not fails else 'Fail' if fails else '-'), 0, 1)
    txt = ('Statement of conformity only applicable on accredited parameters. The statement of compliance is based on a 95% coverage probability for the expanded uncertainty. ')
    if passes:
        txt += 'The measured value of %s along with their respective uncertainty bands were within the acceptance limit, therefore these parameters are considered as Pass (accepted based on guard band). ' % ', '.join(passes)
    if fails:
        txt += 'The measured value of %s along with their respective uncertainty bands were outside the acceptance limit, therefore these parameters are considered as Fail (rejected based on guard band). ' % ', '.join(fails)
    txt += 'Decision rule: %s.' % r0.decision_rule
    pdf.set_font(f, '', 7.8); pdf.set_x(14); pdf.multi_cell(186, 4.2, '-  ' + txt, new_x='LMARGIN', new_y='NEXT')
    top = max(pdf.get_y() + 6, _FOOT_TOP - 34)
    if top + _SIG_MIN > _FOOT_TOP + 2:
        pdf.add_page(); top = pdf.get_y() + 3
    pdf.set_auto_page_break(False)
    def first(attr_u, attr_at, attr_name):
        for r in recs:
            if getattr(r, attr_at) and getattr(r, attr_u):
                return _uname(getattr(r, attr_u)), _sig_image(getattr(r, attr_u)), False
        for r in recs:
            if getattr(r, attr_name):
                return getattr(r, attr_name), None, True
        return '', None, any(r.inducted for r in recs)
    roles = _ROLES.get(loc, _ROLES['Karachi'])
    _panels(pdf, f, [('Analyzed By', roles[0]) + first('performed_by', 'performed_at', 'performed_name'),
                     ('Reviewed By', roles[1]) + first('reviewed_by', 'reviewed_at', 'reviewed_name'),
                     ('Approved By', roles[2]) + first('approved_by', 'approved_at', 'approved_name')], top, max(_SIG_MIN, _FOOT_TOP - top), LINE, GREY)
    return _resp(pdf, 'Decision_rule_report_%s_%s' % (loc, sample_id))


def soc_request_pdf(request, pk):
    """ETAL-LAB-708-FF-17 laid out as the laboratory's controlled Word form (Karachi and Lahore versions)."""
    from QC.soc_ff17 import build_ff17
    q = get_object_or_404(SocRequest, pk=pk)
    if not _can_view(request.user, q.location):
        return _denied_view(request, q.location)
    ctrl = _docctrl('soc_request', q.location, q.date)
    signer, img = '', None
    if q.authorised_at and q.authorised_by:
        signer = '%s  %s' % (_uname(q.authorised_by), _tz.localtime(q.authorised_at).strftime('%d-%m-%Y'))
        img = _sig_image(q.authorised_by)
    elif q.inducted:
        signer = 'Signed on the paper form'
    pdf = build_ff17(q, ctrl, signer, img, watermark='' if (q.decision and (q.authorised_at or q.inducted)) else 'DRAFT')
    return _resp(pdf, 'SOC_request_%s_%s' % (q.location, q.sample_id))
