"""GrowVana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:    path('dashboard/', include('dashboard.urls')),
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('capteurs/', include('capteurs.urls')),
    path('culture/', include('culture.urls')),
    path('mesures/', include('mesures.urls')),
    path('notifications/', include('notification.urls')),
    path('historique/', include('historique.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('landing_page.urls')),
]
