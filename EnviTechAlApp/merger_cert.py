from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from .models import *
import traceback
import sys
import fitz  # PyMuPDF
import os


# ─────────────────────────────────────────────────────────────────────────────
# Certificate mapping
# ─────────────────────────────────────────────────────────────────────────────

def get_certificate_mapping():
    from .views import (
        calib_pdf,
        inspect_pdf,
        verif_pdf,
    )
    return {
        'calib': (Calibration, calib_pdf, 'Calibration Certificate'),
        'insp': (Inspection, inspect_pdf, 'Inspection Certificate'),
        'verif': (Verification, verif_pdf, 'Verification Certificate'),
    }


# ─────────────────────────────────────────────────────────────────────────────
# PDF retrieval
# ─────────────────────────────────────────────────────────────────────────────

def get_pdf_bytes_for_certificate(cert_num, request):
    """Find certificate by cert_num across all models and return its PDF bytes."""
    mapping = get_certificate_mapping()

    for cert_type, (model, generate_fn, cert_name) in mapping.items():
        try:
            certificate = model.objects.get(cert_num=cert_num)
            print(f"✓ Found {cert_num} in {cert_name}")
            cert_id = certificate.id

            import inspect
            if 'return_bytes' in inspect.signature(generate_fn).parameters:
                pdf_bytes = generate_fn(request, cert_id, return_bytes=True)
            else:
                response = generate_fn(request, cert_id)
                if hasattr(response, 'content'):
                    pdf_bytes = BytesIO(response.content)
                else:
                    return False, "Function didn't return a valid response", cert_name

            if pdf_bytes and isinstance(pdf_bytes, BytesIO):
                pdf_bytes.seek(0)
                if pdf_bytes.read(4) == b'%PDF':
                    pdf_bytes.seek(0)
                    print(f"  ✓ Valid PDF generated")
                    return True, pdf_bytes, cert_name
                else:
                    return False, "Generated content is not a valid PDF", cert_name
            else:
                return False, f"PDF generation returned {type(pdf_bytes)}", cert_name

        except model.DoesNotExist:
            continue
        except Exception as e:
            return False, f"Error in {cert_name}: {str(e)}", cert_name

    return False, f"Certificate {cert_num} not found in any model", None


# ─────────────────────────────────────────────────────────────────────────────
# Compression helpers
# ─────────────────────────────────────────────────────────────────────────────

def _size_mb(data: bytes) -> float:
    return len(data) / (1024 * 1024)


def stage1_structural_compress(pdf_bytes: BytesIO) -> BytesIO:
    """
    Stage 1 – Lossless structural optimisation via PyMuPDF.
    Removes unused objects, deduplicates, and deflates streams/fonts.
    Zero quality loss; typically shrinks text-heavy PDFs by 20–50 %.
    """
    pdf_bytes.seek(0)
    doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")

    out = BytesIO()
    doc.save(
        out,
        garbage=4,          # remove unused objects + deduplicate
        deflate=True,       # compress content streams
        deflate_images=True, # compress image streams (lossless zlib)
        deflate_fonts=True,  # compress embedded font streams
        clean=True,         # sanitise content streams
        pretty=False,       # compact output
        linear=False,       # not needed for email/download
    )
    doc.close()
    out.seek(0)
    return out


def stage2_image_compress(pdf_bytes: BytesIO, quality: int = 85) -> BytesIO:
    """
    Stage 2 – Re-encode large embedded images as JPEG at the given quality.
    Images < 20 KB are left untouched so icons/logos stay sharp.
    quality=85 is visually lossless for most lab-report imagery.
    """
    pdf_bytes.seek(0)
    doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")

    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)

                # Skip tiny images (icons, bullets, borders)
                if pix.size < 20_000:
                    pix = None
                    continue

                # Skip CMYK – converting may shift colours
                if pix.n - pix.alpha >= 4:
                    pix = None
                    continue

                # Ensure RGB (drop alpha channel if present)
                if pix.alpha:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                jpeg_bytes = pix.tobytes("jpeg", quality=quality)
                pix = None

                # Only replace if JPEG is actually smaller
                original_len = len(doc.xref_stream(xref))
                if len(jpeg_bytes) < original_len:
                    doc.update_stream(xref, jpeg_bytes)

            except Exception:
                continue  # leave image unchanged on any error

    out = BytesIO()
    doc.save(out, garbage=3, deflate=True, clean=True)
    doc.close()
    out.seek(0)
    return out


def stage3_image_compress_aggressive(pdf_bytes: BytesIO, quality: int = 65) -> BytesIO:
    """
    Stage 3 – More aggressive image re-encoding for stubborn large PDFs.
    Only triggered when stages 1 + 2 still exceed the size target.
    quality=65 still looks acceptable in print/screen at A4 size.
    """
    return stage2_image_compress(pdf_bytes, quality=quality)


# ─────────────────────────────────────────────────────────────────────────────
# Main compression orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def compress_pdf(pdf_bytes: BytesIO, target_mb: float = 5.0) -> BytesIO:
    """
    Multi-stage, quality-preserving compression pipeline.

    Stage 1  – Lossless structural optimisation (always runs)
    Stage 2  – High-quality image re-encoding (quality=85, runs if > target)
    Stage 3  – Medium-quality image re-encoding (quality=65, last resort)

    Pages are NEVER rasterised, so text/vector quality is always preserved.
    """
    start_mb = _size_mb(pdf_bytes.getvalue())
    print(f"\n  📦 Compression pipeline (target ≤ {target_mb} MB)")
    print(f"     Input  : {start_mb:.2f} MB")

    # ── Stage 1: lossless structural
    result = stage1_structural_compress(pdf_bytes)
    s1_mb = _size_mb(result.getvalue())
    print(f"     Stage 1 (lossless): {s1_mb:.2f} MB  {'✓' if s1_mb <= target_mb else '→ continuing'}")

    if s1_mb <= target_mb:
        return result

    # ── Stage 2: high-quality image recompression
    result = stage2_image_compress(result, quality=85)
    s2_mb = _size_mb(result.getvalue())
    print(f"     Stage 2 (img q=85): {s2_mb:.2f} MB  {'✓' if s2_mb <= target_mb else '→ continuing'}")

    if s2_mb <= target_mb:
        return result

    # ── Stage 3: medium-quality image recompression
    result = stage3_image_compress_aggressive(result, quality=65)
    s3_mb = _size_mb(result.getvalue())
    print(f"     Stage 3 (img q=65): {s3_mb:.2f} MB  {'✓' if s3_mb <= target_mb else '⚠ still above target'}")

    if s3_mb > target_mb:
        print(
            f"     ⚠ Could not reach {target_mb} MB without rasterising pages.\n"
            f"       Final size: {s3_mb:.2f} MB — text/vector quality is fully preserved.\n"
            f"       Tip: reduce the number of selected certificates to stay under {target_mb} MB."
        )

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────────────

def merge_pdfs_cert(
    selected_certs: list,
    request,
    pdf_password: str = "1234",
    compress: bool = True,
    target_size_mb: float = 5.0,
) -> BytesIO:
    """
    Merge multiple certificates (identified by cert_num) into a single
    password-protected, compressed PDF.
    """
    print(f"\n{'='*60}")
    print(f"  Merging {len(selected_certs)} certificate(s)")
    print(f"{'='*60}")

    merged_writer = PdfWriter()

    for idx, cert_num in enumerate(selected_certs, 1):
        if not cert_num:
            continue

        print(f"\n[{idx}] {cert_num}")
        success, result, cert_name = get_pdf_bytes_for_certificate(cert_num, request)

        if not success:
            print(f"  ✗ Skipped — {result}")
            continue

        try:
            result.seek(0)
            reader = PdfReader(result)

            # Decrypt if source PDF is password-protected
            if reader.is_encrypted:
                for pwd in ["karachi123", "1234"]:
                    try:
                        if reader.decrypt(pwd):
                            break
                    except Exception:
                        continue

            for page in reader.pages:
                merged_writer.add_page(page)

            print(f"  ✓ Added {len(reader.pages)} page(s) — {cert_name}")

        except Exception as e:
            print(f"  ✗ Error reading {cert_name}: {e}")
            continue

    # Write raw merged PDF
    raw_buffer = BytesIO()
    merged_writer.write(raw_buffer)
    raw_buffer.seek(0)

    raw_mb = _size_mb(raw_buffer.getvalue())
    print(f"\n  Raw merged size : {raw_mb:.2f} MB")

    # ── Compress ────────────────────────────────────────────────────────────
    if compress:
        compressed_buffer = compress_pdf(raw_buffer, target_mb=target_size_mb)
    else:
        compressed_buffer = raw_buffer

    # ── Re-encrypt ──────────────────────────────────────────────────────────
    try:
        compressed_buffer.seek(0)
        enc_reader = PdfReader(compressed_buffer)
        enc_writer = PdfWriter()

        for page in enc_reader.pages:
            enc_writer.add_page(page)

        enc_writer.encrypt(
            user_password=pdf_password,
            owner_password="karachi123",
            use_128bit=False,
        )

        final_buffer = BytesIO()
        enc_writer.write(final_buffer)
        final_buffer.seek(0)

    except Exception as e:
        print(f"  ⚠ Encryption warning: {e} — returning unencrypted PDF")
        compressed_buffer.seek(0)
        final_buffer = compressed_buffer

    final_mb = _size_mb(final_buffer.getvalue())
    print(f"  Final size      : {final_mb:.2f} MB")
    print(f"{'='*60}\n")

    return final_buffer