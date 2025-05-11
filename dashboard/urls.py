from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('stats/', views.dashboard_stats, name='stats'),
    path('devices/', views.dashboard_devices, name='devices'),
    path('notifications/', views.dashboard_notifications, name='notifications'),
    path('settings/', views.dashboard_settings, name='settings'),

    # Admin dashboard
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:user_id>/cultures/', views.admin_user_cultures, name='admin_user_cultures'),
    path('admin/users/<int:user_id>/capteurs/', views.admin_user_capteurs, name='admin_user_capteurs'),
    path('admin/users/<int:user_id>/mesures/', views.admin_user_mesures, name='admin_user_mesures'),
    path('admin/users/<int:user_id>/alertes/', views.admin_user_alerts, name='admin_user_alerts'),

    # Notifications CRUD
    path('notifications/create/', views.notifications_create, name='notifications_create'),
    path('notifications/<int:alert_id>/', views.notifications_detail, name='notifications_detail'),
    path('notifications/<int:alert_id>/delete/', views.notifications_delete, name='notifications_delete'),

    # Devices CRUD
    path('devices/create/', views.devices_create, name='devices_create'),
    path('devices/<int:capteur_id>/', views.devices_detail, name='devices_detail'),
    path('devices/<int:capteur_id>/delete/', views.devices_delete, name='devices_delete'),
    path('devices/<int:capteur_id>/update_status/', views.devices_update_status, name='devices_update_status'),
]
