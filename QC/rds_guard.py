"""RDS record integrity (QA audit 27-10-2026, release R2): what may be saved and who may open an RDS.

- RDS-18: a save needs a known sample of the user's laboratory and at least one parameter row; errors come back as a
  JSON message the page shows (they used to open as a file).
- RDS-19: every save is kept as a numbered revision of the sample's RDS; Testing Results and the lists use the latest.
- RDS-29: an RDS PDF opens only for the user's laboratory, and a missing record is a "not found" page.
"""
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse

from EnviTechAlApp.models import DrinkingWaterForm, WasteWaterForm2, Sample_registration


def user_lab(request):
    from QC.views.ww import _rds_ww_lab
    return _rds_ww_lab(request)


def sample_city(kind, sample_id):
    """The laboratory (city_location) of the sample's report; None when there is no report for it."""
    model = WasteWaterForm2 if kind == 'ww' else DrinkingWaterForm
    rec = model.objects.filter(sample_id=sample_id).order_by('-id').only('city_location').first()
    return (rec.city_location or '').strip() if rec else None


def _err(message, status=400):
    return JsonResponse({'status': 'error', 'message': message}, status=status)


def check_save(request, kind, sample_id, data):
    """None when the RDS may be saved, otherwise the JSON error response."""
    sample_id = (sample_id or '').strip() if isinstance(sample_id, str) else sample_id
    if not sample_id:
        return _err('Select a sample before saving the RDS.')
    city = sample_city(kind, sample_id)
    if city is None and not Sample_registration.objects.filter(sample_id=sample_id).exists():
        return _err(f'Sample {sample_id} was not found.')
    lab = user_lab(request)
    if lab and city and city.lower() != lab.lower():
        return _err(f'Sample {sample_id} belongs to the {city} laboratory.', 403)
    if not any(k.startswith(('parameter_', 'date_')) for k in data):
        return _err('The RDS has no parameter rows to save.')
    return None


def pdf_record(request, model, kind, pk):
    """The RDS record to print, for the user's laboratory only."""
    rec = model.objects.filter(pk=pk).first()
    if rec is None:
        raise Http404('RDS not found')
    lab = user_lab(request)
    city = sample_city(kind, rec.sample_id)
    if lab and city and city.lower() != lab.lower():
        raise PermissionDenied('This RDS belongs to another laboratory.')
    return rec


def latest(model, sample_id):
    return model.objects.filter(sample_id=sample_id).order_by('-id').first()


def with_revisions(qs):
    """List rows with their revision number per sample (Rev. 1 = first save) and whether they are the latest."""
    rows = list(qs)
    order = {}
    for r in sorted(rows, key=lambda r: r.id):
        order.setdefault(r.sample_id, []).append(r.id)
    for r in rows:
        ids = order[r.sample_id]
        r.rev = ids.index(r.id) + 1
        r.is_latest = r.id == ids[-1]
    return rows


def sample_ids_for_lab(model, kind, request):
    """Distinct sample IDs with an RDS, limited to the user's laboratory."""
    ids = list(dict.fromkeys(model.objects.order_by('-id').values_list('sample_id', flat=True)))
    lab = user_lab(request)
    if not lab:
        return ids
    form = WasteWaterForm2 if kind == 'ww' else DrinkingWaterForm
    own = set(form.objects.filter(city_location__iexact=lab).values_list('sample_id', flat=True))
    return [s for s in ids if s in own]
