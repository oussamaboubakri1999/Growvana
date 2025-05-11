from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('stats/', views.dashboard_stats, name='stats'),
    path('settings/', views.dashboard_settings, name='settings'),
    path('devices/', views.dashboard_devices, name='devices'),
    path('notifications/', views.dashboard_notifications, name='notifications'),
]
