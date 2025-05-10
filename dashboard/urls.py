from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard-home'),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
]
