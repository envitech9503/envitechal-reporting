"""
NonEditableReportMiddleware — hardens ONLY the three pilot report PDFs so a
normal user cannot edit the results in a free tool before printing.

Pilot scope (by URL name): Viscous Liquid, Polybag, Machine Oil (print + report).
Method: text -> vector outlines (Ghostscript) so there is no editable text,
then AES-256 owner-permission lock (edit/copy/annotate OFF, print ON, opens
with no password). FAILS OPEN: if hardening errors for any reason, the
original PDF is delivered unchanged, so report delivery is never broken.
"""
import io
import os
import subprocess
import tempfile
import logging

import pikepdf

log = logging.getLogger(__name__)

_TARGETS = {
    "viscousLiquid-PdfPrint", "viscousLiquid-PdfReport",
    "packingpolybagReport-pdfPrint", "packingpolybagReport-pdfReport",
    "machineOilReport-pdfPrint", "machineOilReport-pdfReport",
}

_PW_FILE = "/home/django/EnviTechAlApp/.pdf_owner_pw"


def _owner_pw():
    try:
        if os.path.exists(_PW_FILE):
            return open(_PW_FILE).read().strip()
    except Exception:
        pass
    return os.environ.get("ETAL_PDF_OWNER_PW", "")


def make_noneditable_bytes(pdf_bytes, owner_pw):
    """Return a hardened copy: vector-outlined + AES-256 edit-locked."""
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "in.pdf")
        out = os.path.join(d, "out.pdf")
        with open(src, "wb") as f:
            f.write(pdf_bytes)
        subprocess.run(
            ["gs", "-o", out, "-sDEVICE=pdfwrite", "-dNoOutputFonts",
             "-dCompatibilityLevel=1.7", "-dPDFSETTINGS=/prepress",
             "-dBATCH", "-dNOPAUSE", "-dQUIET", src],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=60,
        )
        pdf = pikepdf.open(out)
        perms = pikepdf.Permissions(
            extract=False, modify_annotation=False, modify_assembly=False,
            modify_form=False, modify_other=False,
            print_lowres=True, print_highres=True, accessibility=True,
        )
        buf = io.BytesIO()
        pdf.save(buf, encryption=pikepdf.Encryption(
            owner=owner_pw, user="", aes=True, R=6, allow=perms))
        pdf.close()
        return buf.getvalue()


class NonEditableReportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            match = getattr(request, "resolver_match", None)
            if match is None or match.url_name not in _TARGETS:
                return response
            owner = _owner_pw()
            if not owner:
                return response
            if getattr(response, "streaming", False):
                return response
            ctype = response.get("Content-Type", "") if hasattr(response, "get") else ""
            content = getattr(response, "content", b"")
            if "application/pdf" in ctype and content[:4] == b"%PDF":
                hardened = make_noneditable_bytes(content, owner)
                response.content = hardened
                response["Content-Length"] = str(len(hardened))
        except Exception:
            log.exception("NonEditableReport hardening failed; original PDF served")
        return response
