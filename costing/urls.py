from django.urls import path
from . import views

app_name = 'costing'
urlpatterns = [
    path('', views.costing_list, name='list'),
    path('<int:pk>/', views.costing_detail, name='detail'),
    path('api/<int:pk>/recompute/', views.api_recompute, name='api_recompute'),
]
