"""{% doc_ctrl "logging_sheet" "Karachi" "issue_date" %} - a field of the controlled form's revision in force today
(Document Control register, 23-10-2026): create forms carry the current revision, saved records keep theirs."""
from django import template

register = template.Library()


@register.simple_tag
def doc_ctrl(module, location, field, default=''):
    try:
        from EnviTechAlApp import doccontrol as DC
        v = DC.doc_control(module, location, None).get(field)
        if v in (None, '', 'TBA', '-'):
            return default
        return v
    except Exception:
        return default
