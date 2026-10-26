"""Controlled-form document numbers with revision history (owner decision 23-10-2026).

Every module (control charts, Internal Audit, MOU, reagent preparation, chemicals, equipment, job completion,
logging sheet, QC printouts) asks this module for the document-control box of a form:

    doc_control(module, location, on_date)  ->  {'doc_no', 'issue_date', 'issue_no', 'rev_no', 'set', 'rev_id', 'effective_from'}

`on_date` is the DOCUMENT'S OWN DATE (report / audit / NC / study date; a control-chart sheet: the end of its period, at most today);
the revision in force on that date is returned, so issuing a new revision never changes documents dated before
its effective date. A document dated before the first recorded revision gets the first revision.

Changes are made on the Document Control register (issue_revision / correct_revision). Saves made through the
older per-module pages still work: a change of InventoryDocControl is recorded as a new revision effective today
(post_save signal below), so no path can overwrite history.
"""
import datetime as _dt

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

BASELINE = _dt.date(2000, 1, 1)          # effective date of the revision in force before revision history existed
FIELDS = ('doc_no', 'issue_date', 'issue_no', 'rev_no')


def _day(d):
    if d is None:
        return _dt.date.today()
    if isinstance(d, _dt.datetime):
        try:
            from django.utils import timezone
            d = timezone.localtime(d) if timezone.is_aware(d) else d
        except Exception:
            pass
        return d.date()
    if isinstance(d, _dt.date):
        return d
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y'):
        try:
            return _dt.datetime.strptime(str(d).strip()[:10], fmt).date()
        except (TypeError, ValueError):
            continue
    return _dt.date.today()


def _key(module, location):
    """Revision key. A control chart's own form (cc_chart_<pk>) belongs to the chart, not to a laboratory: its
    history is kept under '*' so it survives a change of the chart's laboratory."""
    return (module, '*') if str(module).startswith('cc_chart_') else (module, location)


def own_form(module):
    """Forms that only some documents carry (a chart's own form): no revision on a date means 'not in use then'."""
    return str(module).startswith('cc_chart_')


def default_for(module, location):
    """The numbers each reader printed before revision history (the module's built-in default), or None."""
    try:
        if module == 'control_chart' and location == 'Karachi':
            from QC.views.control_chart import _CC_FORM
            return dict(_CC_FORM)
        if module == 'mou' and location == 'Karachi':
            from QC.views.mou import _MOU_FORM
            return dict(_MOU_FORM)
        if module.startswith('mrm_') and location in ('Karachi', 'Lahore'):
            from QC.views.mrm import _FORMS, _DEFAULT_CTRL
            f = module[4:]
            if f in _FORMS:
                d0 = _DEFAULT_CTRL.get((f, location))
                return {'doc_no': _FORMS[f][0], 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]} if d0 else {'doc_no': _FORMS[f][0]}
        if module.startswith('soc_'):
            from QC.views.soc import _FORMS
            if module in _FORMS and location in _FORMS[module][2]:
                no, title, per = _FORMS[module]
                d0 = per[location]
                return {'doc_no': no, 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]}
        if module.startswith('ia_') and location in ('Karachi', 'Lahore'):
            from QC.views.ia import _IA_FORMS, _IA_DEFAULT_CTRL
            f = module[3:]
            if f in _IA_FORMS:
                d0 = _IA_DEFAULT_CTRL[f]
                return {'doc_no': _IA_FORMS[f][0], 'issue_date': d0[0], 'issue_no': d0[1], 'rev_no': d0[2]}
    except Exception:
        pass
    return None


def _vals(obj):
    return {f: (getattr(obj, f, '') or '').strip() for f in FIELDS}


def revisions(module, location):
    from EnviTechAlApp.models import DocControlRevision
    module, location = _key(module, location)
    return DocControlRevision.objects.filter(module=module, location=location).order_by('-effective_from', '-id')


def revision_on(module, location, on_date=None, strict=None):
    """The revision in force on a date (None if the form has no revision at all). A document older than the first
    recorded revision gets the first revision, except for an own form (strict): it was not in use then."""
    from EnviTechAlApp.models import DocControlRevision
    d = _day(on_date)
    module, location = _key(module, location)
    qs = DocControlRevision.objects.filter(module=module, location=location)
    r = qs.filter(effective_from__lte=d).order_by('-effective_from', '-id').first()
    if r is None and not (own_form(module) if strict is None else strict):
        r = qs.order_by('effective_from', 'id').first()       # document older than the first recorded revision
    return r


def doc_control(module, location, on_date=None, default=None):
    """Document-control box of a form for a laboratory on the document's own date. `default` (dict with the
    four fields) seeds the first revision when the form has none yet, and fills a blank field of a revision
    exactly as the readers did before revision history (hard-coded numbers move into the register unchanged)."""
    dflt = {f: ((default or {}).get(f) or '') for f in FIELDS}
    try:
        r = revision_on(module, location, on_date)
        if r is None and not own_form(module):
            with transaction.atomic():
                _ensure_baseline(module, location, default)
            r = revision_on(module, location, on_date)
        if r is not None:
            v = _vals(r)
            if not (own_form(module) and not v['doc_no']):           # a withdrawn own form stays blank
                v = {f: v[f] or dflt[f] for f in FIELDS}
            return {'doc_no': v['doc_no'] or 'TBA', 'issue_date': v['issue_date'] or '-', 'issue_no': v['issue_no'] or '01',
                    'rev_no': v['rev_no'] or '00', 'set': bool(v['doc_no']), 'rev_id': r.pk, 'effective_from': r.effective_from}
    except Exception:
        pass
    return {'doc_no': dflt['doc_no'] or 'TBA', 'issue_date': dflt['issue_date'] or '-', 'issue_no': dflt['issue_no'] or '01',
            'rev_no': dflt['rev_no'] or '00', 'set': bool(dflt['doc_no']), 'rev_id': None, 'effective_from': None}


def _ensure_baseline(module, location, default=None):
    """First revision of a form that has none: what was printed so far (InventoryDocControl row, else the reader's
    default, else blank = TBA), effective from the start, so a later revision never reaches older documents."""
    from EnviTechAlApp.models import InventoryDocControl
    if own_form(module) or revisions(module, location).exists():
        return None
    mirror = InventoryDocControl.objects.filter(module=module, location=location).first()
    seed = _vals(mirror) if mirror is not None and (mirror.doc_no or mirror.issue_date) else None
    if seed is None:
        d = default or default_for(module, location)
        seed = {f: ((d or {}).get(f) or '') for f in FIELDS}
    r = _create(module, location, seed, BASELINE, 'Revision in force before revision history (recorded automatically)', None)
    sync_mirror(module, location, None)
    return r


def _create(module, location, vals, effective_from, note, user):
    from EnviTechAlApp.models import DocControlRevision
    module, location = _key(module, location)
    r = DocControlRevision.objects.create(module=module, location=location, effective_from=effective_from, note=(note or '')[:300],
                                          created_by=user if (user is not None and getattr(user, 'is_authenticated', False)) else None,
                                          **{f: (vals.get(f) or '').strip()[:{'doc_no': 60, 'issue_date': 20}.get(f, 10)] for f in FIELDS})
    return r


def sync_mirror(module, location, user=None):
    """InventoryDocControl shows the revision in force today (screens that display 'the current number')."""
    from EnviTechAlApp.models import InventoryDocControl
    r = revision_on(module, location, None)
    if r is None or len(module) > 20:
        return
    m = None
    if own_form(module):                       # the chart's row carries the chart's laboratory
        m = InventoryDocControl.objects.filter(module=module).first()
        if m is None and not (r.doc_no or '').strip():
            return
    if m is None:
        m, _ = InventoryDocControl.objects.get_or_create(module=module, location=location)
    v = _vals(r)
    if _vals(m) != v:
        for f in FIELDS:
            setattr(m, f, v[f])
        if user is not None and getattr(user, 'is_authenticated', False):
            m.updated_by = user
        m._from_register = True
        m.save()


@transaction.atomic
def issue_revision(module, location, vals, effective_from, note, user):
    """A new revision of the form from `effective_from`: documents dated from then on print it; earlier
    documents keep theirs. Returns the new DocControlRevision."""
    eff = _day(effective_from)
    if eff > BASELINE:
        _ensure_baseline(module, location)       # first revision ever: what was printed so far stays with older documents
    r = _create(module, location, vals, eff, note, user)
    sync_mirror(module, location, user)
    return r


@transaction.atomic
def correct_revision(rev, vals, note, user):
    """Correct a typing error in an existing revision (same revision, every document dated in its period follows);
    the previous values stay in the audit history with the reason."""
    for f in FIELDS:
        setattr(rev, f, (vals.get(f) or '').strip()[:{'doc_no': 60, 'issue_date': 20}.get(f, 10)])
    rev.note = ('%s | corrected %s by %s: %s' % (rev.note, _dt.date.today().strftime('%d-%m-%Y'),
                                                 (user.get_full_name() or user.get_username()) if user else 'system', note or ''))[-300:]
    rev._change_reason = note
    rev.save()
    sync_mirror(rev.module, rev.location, user)
    return rev


def seed_own(module, doc_no, note='Own form number from the chart master, in force before revision history (recorded automatically)'):
    """A chart's own number kept only on the chart master becomes its first revision (effective from the start),
    so a later change of the own form never reaches the periods that printed the master number."""
    if not own_form(module) or not (doc_no or '').strip() or revisions(module, '*').exists():
        return None
    return _create(module, '*', {'doc_no': doc_no.strip()}, BASELINE, note, None)


@transaction.atomic
def withdraw(module, location, user, note):
    """An own form stops being used (e.g. a chart goes back to its laboratory's form): an empty revision from today,
    so documents dated earlier keep printing the own form."""
    if not revisions(module, location).exists():
        return None
    cur = revision_on(module, location, None)
    if cur is not None and not (cur.doc_no or '').strip():
        return cur
    return _create(module, location, {f: '' for f in FIELDS}, _dt.date.today(), note, user)


def doc_date(obj, *names):
    """The document's own date: the first of the named attributes that is set, else its creation date, else today."""
    for n in names + ('date', 'created_at'):
        v = getattr(obj, n, None)
        if v:
            return _day(v)
    return _dt.date.today()


def first_saved(obj):
    """Creation date of a record whose `created_at` moves on every save (auto_now): its earliest audit-history
    entry, else `created_at`, else today."""
    try:
        h = obj.history.order_by('history_date').values_list('history_date', flat=True).first()
        if h:
            return _day(h)
    except Exception:
        pass
    return doc_date(obj)


# ---------------------------------------------------------------- older per-module pages keep working
def _on_mirror_saved(sender, instance, created, **kw):
    """A save of InventoryDocControl that did not come from the register (module pages, dashboard, import
    commands) is recorded as a revision: the first values as the baseline, a later change from today."""
    if getattr(instance, '_from_register', False) or kw.get('raw'):
        return
    v = _vals(instance)
    if not (v['doc_no'] or v['issue_date']):
        return
    today = _dt.date.today()
    try:
        with transaction.atomic():
            cur = revision_on(instance.module, instance.location, None)
            if cur is None and not own_form(instance.module) and not revisions(instance.module, instance.location).exists():
                # first values of a form: documents printed so far showed the reader's default (or TBA) - that stays
                # the baseline, the values saved now apply from today
                d = default_for(instance.module, instance.location) or {}
                _create(instance.module, instance.location, {f: d.get(f) or '' for f in FIELDS}, BASELINE,
                        'Revision in force before revision history (recorded automatically)', None)
                cur = revision_on(instance.module, instance.location, None)
            if cur is None or _vals(cur) != v:
                _create(instance.module, instance.location, v, today,
                        ('Own form number set' if own_form(instance.module) else 'Changed') +
                        ' on the module page; applies to documents dated from %s' % today.strftime('%d-%m-%Y'), instance.updated_by)
    except Exception:
        pass


def connect():
    from EnviTechAlApp.models import InventoryDocControl
    post_save.connect(_on_mirror_saved, sender=InventoryDocControl, dispatch_uid='doccontrol_mirror_revision')
