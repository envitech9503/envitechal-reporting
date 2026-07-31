"""Public QR verification (added 31-07-2026).

Scanning the QR printed on a report or certificate must open that document, not
the login page.  The QR encodes a token signed with SECRET_KEY that carries only
the document family and its id, so:

  * it cannot be forged or tampered with (bad signature -> 404), and
  * record ids cannot be enumerated: a token opens exactly one document.

Staff-only chrome (Back / Print / Report / Home) is hidden for public visitors,
so a scan shows the read-only view form and nothing else.
"""
from django.core import signing
from django.shortcuts import render

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
