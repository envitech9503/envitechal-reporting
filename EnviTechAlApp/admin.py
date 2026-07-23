from django.contrib import admin
from EnviTechAlApp.models import *


admin.site.register(DrinkingWaterForm)
class DrinkingWaterAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
admin.site.register(GaseousEmissionForm)
admin.site.register(AmbientAirForm)
admin.site.register(WasteWaterSludge)
admin.site.register(VehiculEmissionForm)
admin.site.register(LuxAnalysisForm)
admin.site.register(PackingPolyBagForm)
admin.site.register(MachineOilForm)
admin.site.register(MicrobialAnalysis)
admin.site.register(ViscousLiquid)
admin.site.register(AmbientAir2)
admin.site.register(WasteWaterForm2)
admin.site.register(NoiseAnalysis)
admin.site.register(Calibration)
admin.site.register(Inspection)
admin.site.register(Verification)
admin.site.register(Customer)
admin.site.register(Sample_registration)
admin.site.register(AuditLog)
admin.site.register(LoggingSheet)
admin.site.register(Signatures)
admin.site.register(Role)
admin.site.register(Industry_sector)
admin.site.register(NoiseMonitoring)
admin.site.register(ClientDetails)
admin.site.register(JobCompletionForm)

admin.site.site_header= 'Envi Tech AL'
admin.site.site_title= 'Envi Tech AL'
admin.site.index_title= 'Administration'

# Reagent & Standards Preparation (additive)
for _m in (ReagentPrep, ReagentPrepChemical, ReagentStandardisation):
    try:
        admin.site.register(_m)
    except admin.sites.AlreadyRegistered:
        pass
