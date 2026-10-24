"""{% load office_tags %} - {% if request.user|can_switch_network %} shows the Office Network menu entry (24-10-2026)."""
from django import template

from EnviTechAlApp.office_ip import can_switch

register = template.Library()


@register.filter
def can_switch_network(user):
    return can_switch(user)
