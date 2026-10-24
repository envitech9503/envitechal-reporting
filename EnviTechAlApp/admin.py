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

# Reagent prep audit (round 2)
try:
    from EnviTechAlApp.models import ReagentPrepAudit as _RPA
    from django.contrib import admin as _adm
    try:
        _adm.site.register(_RPA)
    except Exception:
        pass
except Exception:
    pass

# Reagent standardisation history (round 2b)
try:
    from EnviTechAlApp.models import ReagentStandardisationHistory as _RSH
    from django.contrib import admin as _adm2
    try:
        _adm2.site.register(_RSH)
    except Exception:
        pass
except Exception:
    pass


# ---------------------------------------------------------------- users: retire, never delete (24-10-2026)
from django.contrib import messages as _messages
from django.contrib.auth import get_user_model as _get_user_model
from django.contrib.auth.admin import UserAdmin as _BaseUserAdmin
from django.http import HttpResponseRedirect as _Redirect

from EnviTechAlApp.user_retire import retire as _retire, protected as _protected

_U = _get_user_model()


class RetireUserAdmin(_BaseUserAdmin):
    """User accounts are retired, never deleted, so that every report, e-signature, log and trace keeps the person's
    name (EnviTechAlApp/user_retire.py). The list shows active users unless 'Active: No' / 'All' is chosen."""
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'last_login')
    actions = ['retire_selected']

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if request.method == 'GET' and not any(k.startswith('is_active') for k in request.GET) and not request.GET.get('q'):
            q = request.GET.copy(); q['is_active__exact'] = '1'
            return _Redirect('%s?%s' % (request.path, q.urlencode()))
        return super().changelist_view(request, extra_context)

    @admin.action(description='Retire selected users (left the company - records, signatures and logs are kept)')
    def retire_selected(self, request, queryset):
        done, skipped = [], []
        for u in queryset:
            if u.pk == request.user.pk or _protected(u):
                skipped.append(u.username); continue
            if _retire(u, by=request.user, reason='retired from the user list'):
                self.log_change(request, u, 'Retired (left the company): deactivated, rights removed; records kept.')
                done.append(u.username)
        if done:
            self.message_user(request, 'Retired: %s. Their reports, e-signatures, logs and names stay in the system.' % ', '.join(done), _messages.SUCCESS)
        if skipped:
            self.message_user(request, 'Not retired (your own account or the CEO account): %s.' % ', '.join(skipped), _messages.WARNING)


try:
    admin.site.unregister(_U)
except admin.sites.NotRegistered:
    pass
admin.site.register(_U, RetireUserAdmin)
