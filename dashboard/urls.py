from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/filter/', views.get_reports_data, name='filter'),
    
]