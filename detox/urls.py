from django.urls import path
from . import views

urlpatterns = [
    
    path('detox', views.detox, name='detox'),
    path('create_detox', views.create_detox, name='create_detox'),
    path('detoxList', views.detoxList, name='detoxList'),
    path('create_view_detox/<str:pk>/', views.create_view_detox, name='create_view_detox'),
    path('detox_edit/<str:pk>/', views.detox_edit, name='detox_edit'),
    path('detox_edit_update/<str:pk>/', views.detox_edit_update, name='detox_edit_update'),
    path('detox_clone/<str:pk>/', views.detox_clone, name='detox_clone'),
    path('detox_clone_update/<str:pk>/', views.detox_clone_update, name='detox_clone_update'),
    path('detox_delete/<str:pk>/', views.detox_delete, name='detox_delete'),
    path('detox_pdf/<str:pk>/', views.detox_pdf, name='detox_pdf'),
]