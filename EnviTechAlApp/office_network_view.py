"""Office-network protection - administrator page (24-10-2026).

/office-network/ : the switch holders (settings.OFFICE_SWITCH_USERS - the CEO, Sana and Hina) turn the static-IP protection ON or OFF for each office and correct an
office's internet IP; every change needs a reason and is written to OfficeNetworkLog. Rule: EnviTechAlApp/office_ip.py.
"""
import ipaddress

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from EnviTechAlApp import office_ip as oip
from EnviTechAlApp.models import OfficeNetwork, OfficeNetworkLog


def _uname(u):
    return ((u.get_full_name() or u.username).strip() if u else '')


def _public_ip(v):
    try:
        a = ipaddress.ip_address(v)
    except ValueError:
        return None
    if a.is_private or a.is_loopback or a.is_unspecified or a.is_multicast or a.is_reserved or a.is_link_local:
        return None
    return str(a)


def _holders():
    from django.conf import settings
    names = {n.lower() for n in getattr(settings, 'OFFICE_SWITCH_USERS', [])}
    return [_uname(u) for u in User.objects.filter(is_active=True) if u.username.lower() in names]


@login_required
def office_network(request):
    if not oip.can_switch(request.user):
        return HttpResponseForbidden('<h2 style="font-family:sans-serif">Not permitted</h2>'
                                     '<p style="font-family:sans-serif">Office network access is managed by the CEO, Sana Ashraf and Hina Abidi.</p>')
    here = oip.client_ip(request)
    if request.method == 'POST':
        loc = request.POST.get('location', '')
        act = request.POST.get('action', '')
        reason = (request.POST.get('reason') or '').strip()[:300]
        o = OfficeNetwork.objects.filter(location=loc).first()
        if not o or act not in ('on', 'off', 'ip'):
            messages.error(request, 'Unknown office or action.')
            return redirect('office_network')
        if len(reason) < 5:
            messages.error(request, 'Please give a reason (at least 5 characters) - it is kept in the change log.')
            return redirect('office_network')
        old = new = ''
        if act in ('on', 'off'):
            want = act == 'on'
            if o.enforced == want:
                messages.info(request, 'The %s protection is already %s.' % (loc, 'ON' if want else 'OFF'))
                return redirect('office_network')
            old, new = ('OFF', 'ON') if want else ('ON', 'OFF')
            o.enforced = want
            o.note = reason
        else:
            ip = _public_ip((request.POST.get('ip_address') or '').strip())
            if not ip:
                messages.error(request, 'Please enter the office\'s public internet IP address (for example 124.29.208.36).')
                return redirect('office_network')
            clash = OfficeNetwork.objects.filter(ip_address=ip).exclude(pk=o.pk).first()
            if clash:
                messages.error(request, '%s is already the IP of the %s office.' % (ip, clash.location))
                return redirect('office_network')
            if ip == o.ip_address:
                messages.info(request, 'The %s IP is already %s.' % (loc, ip))
                return redirect('office_network')
            old, new = o.ip_address, ip
            o.ip_address = ip
        o.updated_by = request.user
        o.save()
        OfficeNetworkLog.objects.create(location=loc, action=act, old_value=old, new_value=new, reason=reason,
                                        user=request.user, user_name=_uname(request.user)[:150], from_ip=here[:45])
        oip.invalidate()
        if act == 'ip':
            messages.success(request, '%s office IP changed from %s to %s.' % (loc, old, new))
        elif act == 'off':
            messages.warning(request, '%s protection is now OFF: %s staff may use the system from any network. '
                                      'Turn it back ON as soon as the office network is available.' % (loc, loc))
        else:
            messages.success(request, '%s protection is now ON: %s staff may use the system only from the office network '
                                      '(within about 10 seconds on every server process).' % (loc, loc))
        return redirect('office_network')

    rules = oip.rules()
    offices = list(OfficeNetwork.objects.select_related('updated_by'))
    staff = {o.location: [] for o in offices}
    unassigned, exempt = [], []
    for u in User.objects.filter(is_active=True).order_by('first_name', 'username'):
        if oip.is_exempt(u):
            exempt.append(_uname(u)); continue
        offs = [x for x in oip.user_offices(u) if x in staff]
        if offs:
            for x in offs:
                staff[x].append(_uname(u) + (' (administrator)' if u.is_superuser else ''))
        else:
            unassigned.append(_uname(u) + (' (administrator)' if u.is_superuser else ''))
    here_office = next((o.location for o in offices if o.ip_address == here), '')
    all_off = bool(offices) and all(not o.enforced for o in offices)
    return render(request, 'office_network.html', {
        'offices': [{'o': o, 'staff': staff.get(o.location, [])} for o in offices],
        'unassigned': unassigned, 'exempt': exempt, 'all_off': all_off,
        'here': here, 'here_office': here_office, 'log': OfficeNetworkLog.objects.select_related('user')[:60],
        'fallback': not offices, 'rules': rules, 'holders': _holders(),
    })
