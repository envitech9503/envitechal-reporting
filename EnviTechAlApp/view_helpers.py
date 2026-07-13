"""Shared view helpers extracted from views.py (refactor rehearsal step 1). Behaviour-identical."""

def _etal_mo_exceeds(res, lim):
    import re as _re
    try:
        rs = str(res).strip().replace(",", "")
        ls = str(lim).strip().replace(",", "")
        if rs.startswith("<"):
            return False
        rm = _re.search(r"-?\d+(?:\.\d+)?", rs)
        lm = _re.search(r"-?\d+(?:\.\d+)?", ls)
        if not rm or not lm:
            return False
        return float(rm.group()) > float(lm.group())
    except Exception:
        return False


def _etal_red_style():
    from fpdf.fonts import FontFace
    return FontFace(color=(190, 0, 0), emphasis="BOLD")
