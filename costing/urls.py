from django.urls import path
from . import views

app_name = 'costing'
urlpatterns = [
    path('', views.costing_list, name='list'),
    path('add/', views.costing_add, name='add'),
    path('<int:pk>/', views.costing_detail, name='detail'),
    path('<int:pk>/edit/', views.costing_edit, name='edit'),
    path('<int:pk>/clone/', views.costing_clone, name='clone'),
    path('<int:pk>/delete/', views.costing_delete, name='delete'),
    path('<int:pk>/history/', views.costing_history, name='history'),
    path('api/<int:pk>/recompute/', views.api_recompute, name='api_recompute'),
]
