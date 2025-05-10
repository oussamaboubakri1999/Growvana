from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('landing_page.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('api/historique/', include('historique.urls')),
    path('accounts/', include('allauth.urls')),
]
