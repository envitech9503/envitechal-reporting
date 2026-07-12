from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/filter/', views.get_reports_data, name='filter'),
    path('audit/', views.audit_page, name='audit'),
    path('api/audit/', views.audit_data, name='audit_data'),
    path('api/audit-detail/', views.audit_detail, name='audit_detail'),
    
]