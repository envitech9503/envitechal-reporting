from django import template

register = template.Library()


@register.filter
def strip_zeros(value):
    """Cosmetically strip trailing zeros from a numeric string
    (e.g. "82.0000" -> "82", "1.50" -> "1.5") while leaving any
    non-numeric entry ("BDL", "<0.001", "-", "N/A", blank) exactly
    as entered. Never raises."""
    try:
        if value is None:
            return value
        s = str(value)
        t = s.strip()
        if t == "":
            return s
        float(t)  # numeric check; raises for non-numeric -> caught below
        if "." in t:
            t = t.rstrip("0").rstrip(".")
            if t in ("", "-", "+", "-.", "+."):
                t = "0"
        return t
    except Exception:
        return value
