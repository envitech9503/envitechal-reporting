from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/filter/', views.get_reports_data, name='filter'),
    path('audit/', views.audit_page, name='audit'),
    path('lifecycle/', views.lifecycle_page, name='lifecycle'),
    path('api/lifecycle/', views.lifecycle_data, name='lifecycle_data'),
    path('api/lifecycle-set/', views.lifecycle_set, name='lifecycle_set'),
    path('equipment/', views.equipment_page, name='equipment'),
    path('api/equipment/', views.equipment_data, name='equipment_data'),
    path('api/equipment-save/', views.equipment_save, name='equipment_save'),
    path('label/', views.sample_label, name='sample_label'),
    path('limits/', views.limits_page, name='limits'),
    path('api/limits/', views.limits_data, name='limits_data'),
    path('api/limits-save/', views.limits_save, name='limits_save'),
    path('api/limits-check/', views.limits_check, name='limits_check'),
    path('api/audit/', views.audit_data, name='audit_data'),
    path('api/audit-detail/', views.audit_detail, name='audit_detail'),
    
]