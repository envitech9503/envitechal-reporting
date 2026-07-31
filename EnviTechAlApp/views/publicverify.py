"""Public QR verification (added 31-07-2026).

Scanning the QR printed on a report or certificate must open that document, not
the login page.  The QR encodes a token signed with SECRET_KEY that carries only
the document family and its id, so:

  * it cannot be forged or tampered with (bad signature -> 404), and
  * record ids cannot be enumerated: a token opens exactly one document.

Staff-only chrome (Back / Print / Report / Home) is hidden for public visitors,
so a scan shows the read-only view form and nothing else.
"""
import re

from django.core import signing
from django.core.cache import cache
from django.shortcuts import redirect, render

from .shared import ETAL_QR_SALT

_INVALID = ('This verification link is not valid. If you received this QR code on '
            'an Envi Tech AL report or certificate, please contact the laboratory.')


def _verify_targets():
    """Resolve target views by module path.

    NB: the views package star-imports every family module, and some function
    names shadow the submodule of the same name (e.g. `inspection`), so
    `from . import inspection` can yield a function.  Import by full module
    path instead - this is shadow-proof.
    """
    from importlib import import_module

    def _v(mod, func):
        return getattr(import_module('EnviTechAlApp.views.' + mod), func)

    return {
        'aa1': _v('ambient', 'ambientAirview'),
        'aa2': _v('ambient', 'ambientAir2View'),
        'dw': _v('misc', 'drinkWaterReport'),
        'mb': _v('microbial', 'microbialView'),
        'ppwr': _v('ppwr', 'ppwrView'),
        'ww1': _v('waste', 'wasteWaterView'),
        'ww2': _v('waste', 'wasteWAter2View'),
        'lux': _v('lux', 'luxAnalysisView'),
        'pack': _v('packing', 'packingPolyBagView'),
        'insp': _v('inspection', 'inspect_view'),
        'verif': _v('verif', 'verif_view'),
        'calib': _v('calib', 'calib_view'),
        'moil': _v('machine', 'machineOilView'),
        'visc': _v('viscous', 'viscousLiquidview'),
        'gas': _v('gaseous', 'gaseousEmissionReport'),
        'na': _v('noise', 'noiseAnalysisView'),
        'nm': _v('noise', 'noiseMonitoring_view'),
        'veh': _v('vehicular', 'vehicularEmissionView'),
    }


def public_verify(request, token):
    try:
        data = signing.loads(token, salt=ETAL_QR_SALT)
    except signing.BadSignature:
        return render(request, 'error.html', {'error': _INVALID}, status=404)
    except Exception:
        return render(request, 'error.html', {'error': _INVALID}, status=404)

    view = _verify_targets().get(data.get('k'))
    if view is None:
        return render(request, 'error.html', {'error': _INVALID}, status=404)

    request.etal_public_verify = True
    response = view(request, data.get('p'))

    # Hide staff-only controls; a public visitor gets the read-only document only.
    try:
        if hasattr(response, 'content') and 'text/html' in (response.get('Content-Type', '') or ''):
            html = response.content.decode('utf-8', 'ignore')
            css = '<style>section.sticky,.noprint{display:none !important;}</style>'
            if '</head>' in html:
                html = html.replace('</head>', css + '</head>', 1)
            else:
                html = css + html
            response.content = html.encode('utf-8')
            if response.has_header('Content-Length'):
                response['Content-Length'] = str(len(response.content))
    except Exception:
        pass
    return response


# --- Legacy QR support (31-07-2026) ------------------------------------------
# QR codes on documents already printed and issued encode the old *staff* URL
# (e.g. /view-form/2276/).  Those carry no secret, so they cannot simply be made
# public: record ids are sequential, and anyone could then read every client's
# report by changing the number.  Instead an unauthenticated scan of a legacy URL
# is sent to a verification gate that asks for the Lab Report No. / Certificate
# No. printed on the same document.  Whoever holds the document can verify it;
# somebody walking ids cannot.  A correct answer mints the normal signed token.
ETAL_LEGACY_SALT = 'etal.legacy.gate'

# Longest prefixes first so e.g. /ambientAir2-view/ never matches /ambientAir-view/.
LEGACY_ROUTES = (
    ('/GaseousForm-view-form/', 'gas'),
    ('/wasteWaterSludge-view/', 'ww1'),
    ('/vehicularEmission-view/', 'veh'),
    ('/packingpolybag-view/', 'pack'),
    ('/viscousLiquid-view/', 'visc'),
    ('/noiseMonitoring_view/', 'nm'),
    ('/verification_view/', 'verif'),
    ('/luxAnalysisReport/', 'lux'),
    ('/ambientAir2-view/', 'aa2'),
    ('/wasteWater2-view/', 'ww2'),
    ('/calibration_view/', 'calib'),
    ('/noiseAnalysis-view/', 'na'),
    ('/inspection_view/', 'insp'),
    ('/ambientAir-view/', 'aa1'),
    ('/machineOil-view/', 'moil'),
    ('/microbial-view/', 'mb'),
    ('/view-form/', 'dw'),
)

# Certificates are identified by their certificate number; reports by lab report no.
_ID_FIELD = {'insp': 'cert_num', 'verif': 'cert_num', 'calib': 'cert_num'}

_MODELS = {
    'aa1': 'AmbientAirForm', 'aa2': 'AmbientAir2', 'dw': 'DrinkingWaterForm',
    'mb': 'MicrobialAnalysis', 'ww1': 'WasteWaterSludge', 'ww2': 'WasteWaterForm2',
    'lux': 'LuxAnalysisForm', 'pack': 'PackingPolyBagForm', 'insp': 'Inspection',
    'verif': 'Verification', 'calib': 'Calibration', 'moil': 'MachineOilForm',
    'visc': 'ViscousLiquid', 'gas': 'GaseousEmissionForm', 'na': 'NoiseAnalysis',
    'nm': 'NoiseMonitoring', 'veh': 'VehiculEmissionForm',
}


def legacy_gate_redirect(path):
    """Map an old staff URL from a printed QR to the verification gate."""
    for prefix, kind in LEGACY_ROUTES:
        if path.startswith(prefix):
            pk = path[len(prefix):].strip('/').split('/')[0]
            if pk:
                token = signing.dumps({'k': kind, 'p': pk}, salt=ETAL_LEGACY_SALT)
                return '/verify-document/' + token + '/'
    return None


def _norm(s):
    """Compare document numbers ignoring case, spaces and punctuation."""
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def _client_ip(request):
    fwd = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return (fwd.split(',')[0].strip() if fwd else request.META.get('REMOTE_ADDR', '')) or 'unknown'


def legacy_verify(request, token):
    try:
        data = signing.loads(token, salt=ETAL_LEGACY_SALT)
    except Exception:
        return render(request, 'error.html', {'error': _INVALID}, status=404)

    kind = data.get('k')
    pk = data.get('p')
    if kind not in _MODELS:
        return render(request, 'error.html', {'error': _INVALID}, status=404)

    is_cert = kind in _ID_FIELD
    ctx = {
        'token': token,
        'label': 'Certificate No.' if is_cert else 'Lab Report No.',
        'doc_word': 'certificate' if is_cert else 'report',
    }

    if request.method == 'POST':
        cache_key = 'etal_verify_gate_%s' % _client_ip(request)
        attempts = cache.get(cache_key, 0)
        if attempts >= 12:
            ctx['error'] = ('Too many attempts from this connection. Please wait a few minutes '
                            'and try again, or contact the laboratory.')
            return render(request, 'verify_gate.html', ctx, status=429)
        supplied = _norm(request.POST.get('docno'))
        actual = ''
        try:
            from .. import models as _m
            obj = getattr(_m, _MODELS[kind]).objects.filter(pk=pk).first()
            if obj is not None:
                actual = _norm(getattr(obj, _ID_FIELD.get(kind, 'lab_report_no'), ''))
        except Exception:
            actual = ''

        if supplied and actual and supplied == actual:
            # Only failures are rate-limited: a client or auditor verifying a whole
            # batch of documents from one office connection must never be locked out.
            cache.delete(cache_key)
            good = signing.dumps({'k': kind, 'p': str(pk)}, salt=ETAL_QR_SALT)
            return redirect('/verify/' + good + '/')

        cache.set(cache_key, attempts + 1, 900)
        # Deliberately identical wording whether or not the record exists.
        ctx['error'] = 'That number does not match this document. Please check and try again.'

    return render(request, 'verify_gate.html', ctx)
