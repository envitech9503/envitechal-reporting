"""
Report verification endpoint for report.envitechal.com.

Read-only Django view. It answers one question, called server-to-server by the
Envi Tech AL WordPress site: "was this report issued by Envi Tech AL, and what
does the record say?"

CONFIRMED ENVIRONMENT (verified on the droplet, 8 Sep 2026)
----------------------------------------------------------
- Real data is PostgreSQL database `django` on localhost. The gunicorn workers
  reach it because their service environment sets USE_POSTGRES=1; this view is
  served by those workers, so it uses PostgreSQL automatically. It needs NO
  database configuration of its own. (A plain `manage.py shell` without that env
  reads an empty leftover db.sqlite3 — ignore that file.)
- 31 report models carry a `lab_report_no` field. The client NAME is the
  report's own `report_to` column (present on 29 of the 31 tables); `customer_id`
  is a dead legacy code (e.g. "5285") that resolves to nothing, so it is only a
  last-resort fallback. Each report also has an inline `address` and `created_at`
  (DateTimeField, auto_now_add). `form_name` is a per-model CLASS ATTRIBUTE
  (e.g. "Drinking Water Form"), not a column, so getattr on an instance works.
- The `Historical*` models are django-simple-history audit snapshots (many rows
  per report, including intermediate edits). They are EXCLUDED here — verifying
  against them would match superseded/partial versions.

WHY IT IS SHAPED THIS WAY
-------------------------
- The browser never calls this. WordPress signs each request with HMAC-SHA256
  over "timestamp.body"; the timestamp is inside the signed material so a
  captured request cannot be replayed after the window.
- A caller must supply the report number AND its issue date. The reply includes
  client name and address (personal data); requiring the date means the caller
  already holds the document and is confirming what they can read on it. IF THE
  DATE REQUIREMENT IS EVER RELAXED, THE DISCLOSURE MUST BE NARROWED TO MATCH.
- Every failure past the signature check -- unknown number, real number with the
  wrong date, malformed input -- returns an identical {"status":"unknown"} so the
  endpoint cannot be walked to discover which numbers exist.
- It writes nothing and defines no models. There is no migration.

THE ISSUE DATE FIELD
--------------------
ETA_VERIFY_DATE_FIELDS lists which fields count as the "issue date" the verifier
types. It MUST be `reporting_date` first -- that is the date printed on the
document (stored as free text like "27-July-2026", parsed here). `created_at` is
the DB row-creation timestamp and is usually a DIFFERENT day, so it is only a
fallback for records with no reporting_date. Set:
    ETA_VERIFY_DATE_FIELDS = ["reporting_date", "created_at"]
Getting this wrong only ever produces false "unknown"s, never a false "valid".

INSTALL  (exact steps + rollback are in DEPLOY-RUNBOOK.md)
---------------------------------------------------------
1. Place this file at EnviTechAlApp/views/verify_api.py
2. In the ROOT urls.py (EnviTechAlApp/urls.py) add, shadow-proof by full path:
       from EnviTechAlApp.views import verify_api
       path("api/verify/", verify_api.verify_report, name="verify_report"),
3. In settings.py:
       ETA_VERIFY_SECRET = os.environ.get("ETA_VERIFY_SECRET", "")   # 64 hex chars
       ETA_VERIFY_DATE_FIELDS = ["created_at"]
   Put the same secret in the gunicorn service environment and in wp-config.php.
   report.envitechal.com is already in ALLOWED_HOSTS (it serves the site).
"""

import hashlib
import hmac
import json
import re
import time
import datetime as _dt

from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# How far the request timestamp may drift from now, in seconds.
_MAX_SKEW = 300
# Cap on rows normalised per model when the fast exact match misses.
_SCAN_CAP = 50

# One uninformative reply for every kind of failure.
_UNKNOWN = {"status": "unknown"}

# Public report-type titles, keyed by model class name. The data has no clean
# title field (the report_type column is a code like "ww2"; pdf_heading is junk),
# and the models' `form_name` reads "X Form" (internal). These are the titles
# shown to a verifier. Any model not listed falls back to a cleaned form_name.
_REPORT_TYPE_LABELS = {
    "DrinkingWaterForm": "Drinking Water Analysis Report",
    "WasteWaterForm2": "Waste Water Analysis Report",
    "WasteWaterSludge": "Waste Water Sludge Analysis Report",
    "GaseousEmissionForm": "Gaseous Emission Analysis Report",
    "AmbientAirForm": "Ambient Air Quality Report",
    "AmbientAir2": "Ambient Air Quality Report",
    "VehiculEmissionForm": "Vehicular Emission Analysis Report",
    "NoiseAnalysis": "Noise Analysis Report",
    "NoiseMonitoring": "Noise Monitoring Report",
    "LuxAnalysisForm": "Illumination (Lux) Analysis Report",
    "MicrobialAnalysis": "Microbial Analysis Report",
    "MachineOilForm": "Machine Oil Analysis Report",
    "ViscousLiquid": "Viscous Liquid Analysis Report",
    "PackingPolyBagForm": "Packing Material Test Report",
    "PPWRAnalysis": "PPWR Analysis Report",
    "Detox": "Detox Analysis Report of Wastewater",
}


def _report_type_label(model, row):
    label = _REPORT_TYPE_LABELS.get(model.__name__)
    if label:
        return label
    # Fallback: turn a "... Form" form_name into "... Analysis Report".
    fn = str(getattr(row, "form_name", "") or "").strip()
    if fn:
        return re.sub(r"\s*Form$", "", fn) + " Analysis Report" if fn.endswith("Form") else fn
    return "Test Report"

# Cache of the models we search, resolved once on first use.
_MODELS_CACHE = None


def _norm(value):
    """Uppercase; strip spaces, slashes, dashes. Mirrors the WordPress side so
    honest formatting differences match without loosening the identifier."""
    return re.sub(r"[\s/\-]", "", (value or "")).upper()


def _report_models():
    """Primary report models: those with a lab_report_no field, excluding the
    django-simple-history `Historical*` snapshot models."""
    global _MODELS_CACHE
    if _MODELS_CACHE is None:
        out = []
        for model in apps.get_models():
            if model.__name__.startswith("Historical"):
                continue
            names = {f.name for f in model._meta.get_fields()}
            if "lab_report_no" in names:
                out.append((model, names))
        _MODELS_CACHE = out
    return _MODELS_CACHE


def _date_field_names(model, field_names):
    configured = list(getattr(settings, "ETA_VERIFY_DATE_FIELDS", []) or [])
    if configured:
        return [f for f in configured if f in field_names]
    return [
        f.name
        for f in model._meta.get_fields()
        if getattr(f, "get_internal_type", lambda: "")() in ("DateField", "DateTimeField")
    ]


# The printed "report date" (reporting_date) is stored as free text, e.g.
# "27-July-2026". A verifier types the date off their document, so we parse
# whatever format the record holds and compare on the calendar date.
_TEXT_DATE_FORMATS = (
    "%d-%B-%Y", "%d-%b-%Y", "%d %B %Y", "%d %b %Y",
    "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%B %d, %Y",
)


def _coerce_iso(value):
    """Return a YYYY-MM-DD string for a date/datetime or a recognised date
    string, else None."""
    if value is None:
        return None
    if isinstance(value, _dt.datetime):
        return value.date().isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    for fmt in _TEXT_DATE_FORMATS:
        try:
            return _dt.datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _date_matches(row, model, field_names, iso_date):
    for name in _date_field_names(model, field_names):
        if _coerce_iso(getattr(row, name, None)) == iso_date:
            return True
    return False


def _find_report(number, iso_date):
    """Return (row, model) for a report whose number AND date both match, else
    (None, None). A real number with the wrong date is treated as no match."""
    target = _norm(number)
    if not target:
        return None, None

    for model, field_names in _report_models():
        candidates = list(model.objects.filter(lab_report_no__iexact=number)[:_SCAN_CAP])
        if not candidates:
            digits = max(re.findall(r"\d+", number) or [""], key=len)
            if len(digits) >= 3:
                candidates = list(
                    model.objects.filter(lab_report_no__icontains=digits)[:_SCAN_CAP]
                )
        for row in candidates:
            if _norm(getattr(row, "lab_report_no", "")) != target:
                continue
            if _date_matches(row, model, field_names, iso_date):
                return row, model
    return None, None


def _signature_ok(request):
    secret = getattr(settings, "ETA_VERIFY_SECRET", "")
    if not secret:
        return False
    timestamp = request.META.get("HTTP_X_ETA_TIMESTAMP", "")
    supplied = request.META.get("HTTP_X_ETA_SIGNATURE", "")
    if not timestamp.isdigit() or not supplied:
        return False
    if abs(time.time() - int(timestamp)) > _MAX_SKEW:
        return False
    raw = request.body or b""
    expected = hmac.new(
        secret.encode("utf-8"),
        (timestamp + ".").encode("utf-8") + raw,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, supplied)


@csrf_exempt
@require_POST
def verify_report(request):
    # A bad/missing signature is the ONLY non-200 case: WordPress treats non-200
    # as "reporting system unreachable" and falls back to its local registry,
    # rather than telling a visitor a genuine report is fake.
    if not _signature_ok(request):
        return JsonResponse({"detail": "unauthorized"}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse(_UNKNOWN, status=200)

    number = str(payload.get("report_number", "")).strip()
    iso_date = str(payload.get("issue_date", "")).strip()

    if not re.fullmatch(r"[A-Za-z0-9/\-]{4,40}", number):
        return JsonResponse(_UNKNOWN, status=200)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso_date):
        return JsonResponse(_UNKNOWN, status=200)

    row, _model = _find_report(number, iso_date)
    if row is None:
        return JsonResponse(_UNKNOWN, status=200)

    return JsonResponse(
        {
            "status": "valid",
            "report_number": str(getattr(row, "lab_report_no", number)),
            "report_type": _report_type_label(_model, row),
            "client_name": str(getattr(row, "report_to", "") or getattr(row, "customer_id", "") or "").strip(),
            "client_address": str(getattr(row, "address", "") or "").strip(),
            "issue_date": iso_date,
            "issued_by": "Envi Tech AL",
        },
        status=200,
    )
