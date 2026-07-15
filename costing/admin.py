from django.contrib import admin
from .models import (CostingConfig, ReagentRate, LabourGrade,
                     CostParameter, RecipeChemical, RecipeLabour)


class RecipeChemInline(admin.TabularInline):
    model = RecipeChemical
    extra = 1
    autocomplete_fields = ['chemical']


class RecipeLabInline(admin.TabularInline):
    model = RecipeLabour
    extra = 1


@admin.register(CostParameter)
class CostParameterAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'matrix', 'batch_size', 'annual_volume', 'active')
    search_fields = ('code', 'name')
    list_filter = ('active', 'matrix', 'location')
    inlines = [RecipeChemInline, RecipeLabInline]


@admin.register(ReagentRate)
class ReagentRateAdmin(admin.ModelAdmin):
    list_display = ('chemical', 'location', 'unit_cost', 'effective_from', 'source')
    list_filter = ('location',)
    search_fields = ('chemical__name', 'source')
    autocomplete_fields = ['chemical']
    list_editable = ('unit_cost',)


@admin.register(LabourGrade)
class LabourGradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'office', 'gross_month', 'is_direct')
    list_filter = ('office', 'is_direct')
    search_fields = ('name',)


@admin.register(CostingConfig)
class CostingConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'electricity_tariff', 'target_margin', 'updated')


# The host Chemical model is not registered in Django admin (the inventory uses
# a bespoke UI), but the costing admin uses autocomplete_fields=['chemical'],
# which requires the target to be registered with search_fields. Register it
# minimally here so autocomplete works; guarded against double registration.
from django.apps import apps as _apps
from django.conf import settings as _settings
_ChemItem = _apps.get_model(getattr(_settings, 'COSTING_CHEMICAL_MODEL', 'dashboard.Chemical'))
if not admin.site.is_registered(_ChemItem):
    @admin.register(_ChemItem)
    class HostChemicalAdmin(admin.ModelAdmin):
        search_fields = ('name',)
        list_display = ('name', 'category', 'unit')
