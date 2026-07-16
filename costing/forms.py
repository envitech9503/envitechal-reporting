"""Forms for the Costing module — parameter form + inline recipe formsets."""
from django import forms
from django.apps import apps
from django.conf import settings
from django.forms import inlineformset_factory
from .models import CostParameter, RecipeChemical, RecipeLabour, LabourGrade

CHEM = apps.get_model(getattr(settings, 'COSTING_CHEMICAL_MODEL', 'dashboard.Chemical'))

_TEXT = {'class': 'inp'}
_NUM = {'class': 'inp', 'inputmode': 'decimal'}


class CostParameterForm(forms.ModelForm):
    class Meta:
        model = CostParameter
        fields = ['code', 'name', 'matrix', 'method', 'location', 'batch_size',
                  'annual_volume', 'electricity_kwh', 'di_water_ml', 'instrument_cost',
                  'waste_cost', 'qc_batch_cost', 'annual_pool', 'tax_category', 'active']
        widgets = {
            'code': forms.TextInput(attrs=_TEXT), 'name': forms.TextInput(attrs=_TEXT),
            'matrix': forms.TextInput(attrs=_TEXT), 'method': forms.TextInput(attrs=_TEXT),
            'location': forms.TextInput(attrs=_TEXT), 'tax_category': forms.TextInput(attrs=_TEXT),
            'batch_size': forms.NumberInput(attrs=_NUM), 'annual_volume': forms.NumberInput(attrs=_NUM),
            'electricity_kwh': forms.NumberInput(attrs=_NUM), 'di_water_ml': forms.NumberInput(attrs=_NUM),
            'instrument_cost': forms.NumberInput(attrs=_NUM), 'waste_cost': forms.NumberInput(attrs=_NUM),
            'qc_batch_cost': forms.NumberInput(attrs=_NUM), 'annual_pool': forms.NumberInput(attrs=_NUM),
        }

    def clean_code(self):
        code = (self.cleaned_data.get('code') or '').strip()
        qs = CostParameter.objects.filter(code__iexact=code)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A parameter with this code already exists.')
        return code


class RecipeChemicalForm(forms.ModelForm):
    class Meta:
        model = RecipeChemical
        fields = ['chemical', 'qty_sample', 'qty_batch']
        widgets = {'chemical': forms.Select(attrs={'class': 'inp'}),
                   'qty_sample': forms.NumberInput(attrs=_NUM),
                   'qty_batch': forms.NumberInput(attrs=_NUM)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chemical'].queryset = CHEM.objects.order_by('name')


class RecipeLabourForm(forms.ModelForm):
    class Meta:
        model = RecipeLabour
        fields = ['grade', 'minutes_sample']
        widgets = {'grade': forms.Select(attrs={'class': 'inp'}),
                   'minutes_sample': forms.NumberInput(attrs=_NUM)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].queryset = LabourGrade.objects.order_by('name')


RecipeChemicalFormSet = inlineformset_factory(
    CostParameter, RecipeChemical, form=RecipeChemicalForm,
    extra=3, can_delete=True)

RecipeLabourFormSet = inlineformset_factory(
    CostParameter, RecipeLabour, form=RecipeLabourForm,
    extra=2, can_delete=True)
