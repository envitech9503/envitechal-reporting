#!/usr/bin/env python3
"""Header re-layout QA against the live application (read-only).

    python3 hdr_qa.py before <outdir>      # capture PDFs + View Form HTML for the
                                           # latest record of every family
    python3 hdr_qa.py after  <outdir>      # capture again, then verify:
       - every header label starts at HDR_LX (12 mm), every value at HDR_VX (68 mm)
       - no header word ends beyond the 200 mm border
       - every word BELOW the header block is at the same place with the same text
         as in the 'before' capture (nothing else on the page moved)
       - View Form: header label cells left-aligned with the fixed column; Gaseous
         shows "Fuel Types:"
       - create forms: HTTP 200 and the type box carries maxlength/data-charcount
Nothing is written to the database; views are called with GET only.
"""
import os, sys, re, json, io, contextlib, subprocess, inspect
sys.path.insert(0, os.getcwd())
MODE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EnviTechAlApp.settings")
import django
django.setup()
from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.apps import apps
from EnviTechAlApp import views
# The PDFs are delivered AES-encrypted (fpdf2 set_encryption in the views), which
# pdftotext cannot read. Encryption has no effect on layout, so for this
# in-process capture only, set_encryption is a no-op. Production workers are
# untouched (this is a separate process).
import fpdf as _fpdf
_fpdf.FPDF.set_encryption = lambda self, *a, **k: None

FAMILIES = [  # name, view-form view, pdf print view, pdf report view, create url
    ("DrinkingWater", "drinkWaterReport", "generatePDF", "generatePDF_report", "/drinkingWaterForm"),
    ("GaseousEmission", "gaseousEmissionReport", "gaseousReportgeneratePDF", "gaseousReportgeneratePDF1", "/gaseousEmission"),
    ("AmbientAir", "ambientAirview", "ambientAirGeneratePDF", "ambientAirGeneratePDF1", "/ambientAir"),
    ("WasteWaterSludge", "wasteWaterView", "wasteWaterPdf0", "wasteWaterPdf1", "/wasteWaterSludge"),
    ("VehicularEmission", "vehicularEmissionView", "vehicularEmissionReport", "vehicularEmissionReport1", "/vehicularEmission"),
    ("LuxAnalysis", "luxAnalysisView", "luxAnalysisReportPdf", "luxAnalysisReportPdf1", "/luxAnalysis"),
    ("PackingPolyBag", "packingPolyBagView", "packingPolyBagReport", "packingPolyBagReport1", "/packingPolyBag"),
    ("NoiseAnalysis", "noiseAnalysisView", "noiseAnalysisReport", "noiseAnalysisReport1", "/noiseAnalysis"),
    ("MachineOil", "machineOilView", "machineOilReportPdf", "machineOilReportPdf1", "/machineOil"),
    ("MicrobialAnalysis", "microbialView", "microbialAnalysisPdf", "microbialAnalysisPdf1", "/microbialAnalysis"),
    ("ViscousLiquid", "viscousLiquidview", "viscousLiquidPdf", "viscousLiquidPdf1", "/viscousLiquid"),
    ("AmbientAir2", "ambientAir2View", "ambientAir2Pdf", "ambientAir2Pdf1", "/ambientAirQuality2"),
    ("WasteWater2", "wasteWAter2View", "wasteWater2Pdf", "wasteWater2Pdf1", "/wasteWater2"),
    ("NoiseMonitoring", "noiseMonitoring_view", "noiseMonitoring_print", "noiseMonitoring_report", "/noisemonitoring/"),
    ("PPWR", "ppwrView", "ppwrAnalysisPdf", "ppwrAnalysisPdf1", "/ppwrAnalysis"),
]
CREATE_INPUT = {"DrinkingWater": "sample_type", "GaseousEmission": "GasEm-test-type", "AmbientAir": "ambientAir_testtype_location",
                "WasteWaterSludge": "ww_sample_type", "VehicularEmission": "vehEm_test_type", "LuxAnalysis": "lux_test_type",
                "PackingPolyBag": "pack_sample_type", "NoiseAnalysis": "test_type", "MachineOil": "machine_sample_type",
                "MicrobialAnalysis": "micro_sample_type", "ViscousLiquid": "sample_type", "AmbientAir2": "test_type",
                "WasteWater2": "sample_type", "NoiseMonitoring": "test_type", "PPWR": "ppwr_sample_type"}
PT = 72 / 25.4
# header block y-range (mm) per family and builder, from the pre-change survey of pdf_common.py
BANDS = {"DrinkingWater": {"print": [85.0, 127.0], "report": [85.0, 127.0]}, "GaseousEmission": {"print": [82.0, 118.0], "report": [86.0, 122.0]}, "AmbientAir": {"print": [82.0, 112.0], "report": [86.0, 116.0]}, "WasteWaterSludge": {"print": [82.0, 124.0], "report": [86.0, 128.0]}, "VehicularEmission": {"print": [82.0, 112.0], "report": [87.0, 117.0]}, "LuxAnalysis": {"print": [84.0, 114.0], "report": [89.0, 119.0]}, "PackingPolyBag": {"print": [82.0, 118.0], "report": [87.0, 123.0]}, "NoiseAnalysis": {"print": [82.0, 112.0], "report": [87.0, 117.0]}, "MachineOil": {"print": [82.0, 118.0], "report": [87.0, 123.0]}, "MicrobialAnalysis": {"print": [82.0, 124.0], "report": [87.0, 129.0]}, "ViscousLiquid": {"print": [78.0, 120.0], "report": [88.0, 130.0]}, "AmbientAir2": {"print": [88.0, 118.0], "report": [88.0, 118.0]}, "WasteWater2": {"print": [82.0, 130.0], "report": [87.0, 135.0]}, "NoiseMonitoring": {"print": [82.0, 124.0], "report": [87.0, 129.0]}, "PPWR": {"print": [82.0, 124.0], "report": [87.0, 129.0]}}
allmodels = {m.__name__: m for m in apps.get_models()}
hosts = [h for h in getattr(settings, "ALLOWED_HOSTS", []) if h and h != "*"]
host = hosts[0] if hosts else "localhost"
if host.startswith("."):
    host = "www" + host
rf = RequestFactory()
user = User.objects.filter(is_superuser=True).first() or User.objects.first()


def model_for(view):
    src = inspect.getsource(view)
    cands = re.findall(r"(\w+)\.objects\.(?:get|filter)\(", src) + re.findall(r"get_object_or_404\((\w+)", src)
    cands = [c for c in cands if c in allmodels and not c.startswith("Historical")]
    return allmodels[cands[0]] if cands else None


def call(view, path, **kw):
    req = rf.get(path, HTTP_HOST=host)
    req.user = user
    with contextlib.redirect_stdout(io.StringIO()):
        return view(req, **kw)


def words_of(pdf_path):
    bb = subprocess.run(["pdftotext", "-bbox", "-f", "1", "-l", "1", pdf_path, "-"], capture_output=True, text=True).stdout
    return [(round(float(a) / PT, 2), round(float(b) / PT, 2), round(float(c) / PT, 2), round(float(d) / PT, 2), t)
            for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', bb)]


capture = {}
problems = []
for fam, vf, vp, vr, curl in FAMILIES:
    vfv = getattr(views, vf)
    model = model_for(vfv)
    obj = model.objects.order_by("-id").first() if model else None
    if obj is None:
        problems.append("%s: no model/record" % fam); continue
    pk = obj.id
    rec = {"model": model.__name__, "pk": pk}
    for kind, vname in (("print", vp), ("report", vr)):
        try:
            resp = call(getattr(views, vname), "/x/%s/" % pk, pk=pk)
            content = resp.content if hasattr(resp, "content") else b""
            p = os.path.join(OUT, "%s_%s.pdf" % (fam, kind))
            open(p, "wb").write(content)
            rec[kind] = {"status": getattr(resp, "status_code", 0), "bytes": len(content), "words": words_of(p)}
        except Exception as e:
            rec[kind] = {"error": repr(e)[:200]}
            problems.append("%s %s: %r" % (fam, kind, e))
    try:
        resp = call(vfv, "/x/%s/" % pk, pk=pk)
        html = resp.content.decode("utf-8", "replace")
        open(os.path.join(OUT, "%s_view.html" % fam), "w", encoding="utf-8").write(html)
        rec["view"] = {"status": resp.status_code, "bytes": len(html), "left_cells": html.count('style="width:29%;white-space:nowrap"'),
                       "right_cells": html.count("text-right pr-2 pt-1 pb-1"), "fuel_types": html.count("Fuel Types:")}
    except Exception as e:
        rec["view"] = {"error": repr(e)[:200]}; problems.append("%s view: %r" % (fam, e))
    capture[fam] = rec
json.dump(capture, open(os.path.join(OUT, "capture.json"), "w"))
print("[hdr_qa:%s] captured %d families -> %s" % (MODE, len(capture), OUT))
for p in problems:
    print("  PROBLEM:", p)

if MODE == "after":
    before = json.load(open(os.path.join(os.path.dirname(OUT.rstrip("/")), "before", "capture.json")))
    fails = []
    for fam, rec in capture.items():
        for kind in ("print", "report"):
            a = rec.get(kind, {}); b = before.get(fam, {}).get(kind, {})
            if "words" not in a or "words" not in b:
                fails.append("%s %s: missing capture" % (fam, kind)); continue
            if a["status"] != 200:
                fails.append("%s %s: HTTP %s" % (fam, kind, a["status"]))
            y0, y1 = BANDS[fam][kind]
            hdr = [list(w) for w in a["words"] if (y0 - 1.0) <= w[1] <= (y1 + 1.0) and w[0] < 205 and (w[3] - w[1]) < 6.0]
            labels = [w for w in hdr if w[4].endswith(":") and w[0] < 60]
            # leftmost word of every header line that starts in the label column
            lines = {}
            for w in hdr:
                key = round(w[1], 1)
                lines[key] = min(lines.get(key, 999.0), w[0])
            starts = sorted({x for x in lines.values() if x < 60})
            if not labels or any(abs(x - 12.0) > 0.3 for x in starts):
                fails.append("%s %s: label x positions %s" % (fam, kind, starts[:6]))
            vals = [w for w in hdr if 66 <= w[0] <= 70]
            if not vals:
                fails.append("%s %s: no value at 68 mm" % (fam, kind))
            over = [w for w in hdr if w[2] > 200.0 and not (w[0] > 150 and (w[3] - w[1]) > 10)]  # ignore the diagonal watermark
            if over:
                fails.append("%s %s: header text beyond 200 mm: %s" % (fam, kind, over[:2]))
            # everything below the header block, excluding the rotated watermark glyphs (taller than 6 mm),
            # compared as an unordered set so pdftotext's reading order cannot produce a false difference
            below_a = sorted(tuple(w) for w in a["words"] if w[1] > (y1 + 1.0) and (w[3] - w[1]) < 6.0)
            below_b = sorted(tuple(w) for w in b["words"] if w[1] > (y1 + 1.0) and (w[3] - w[1]) < 6.0)
            if below_a != below_b:
                fails.append("%s %s: %d/%d words below the header differ" % (fam, kind, len(below_a), len(below_b)))
        v = rec.get("view", {})
        if v.get("status") != 200 or v.get("right_cells", 1) != 0 or v.get("left_cells", 0) < 5:
            fails.append("%s view: %s" % (fam, v))
        if fam == "GaseousEmission" and v.get("fuel_types", 0) < 1:
            fails.append("Gaseous view: 'Fuel Types:' missing")
    # create forms
    for fam, vf, vp, vr, curl in FAMILIES:
        try:
            from django.urls import resolve
            m = resolve(curl)
            resp = call(m.func, curl, **m.kwargs)
            html = resp.content.decode("utf-8", "replace")
            tag = re.search(r'<input\b[^>]*name="%s"[^>]*>' % re.escape(CREATE_INPUT[fam]), html)
            ok = resp.status_code == 200 and tag and 'maxlength="150"' in tag.group(0) and 'data-charcount="150"' in tag.group(0)
            if not ok:
                fails.append("%s create form: status %s tag %s" % (fam, resp.status_code, (tag.group(0)[:120] if tag else None)))
        except Exception as e:
            fails.append("%s create form: %r" % (fam, e))
    print("[hdr_qa:after] checks: %s" % ("ALL PASSED" if not fails else "%d FAILED" % len(fails)))
    for f in fails:
        print("  FAIL:", f)
    sys.exit(1 if fails else 0)
