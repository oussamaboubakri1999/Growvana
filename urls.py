from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('historique/', include('historique.urls')),
    path('capteurs/', include('capteurs.urls')),
    path('culture/', include('culture.urls')),
    path('mesures/', include('mesures.urls')),
    path('notification/', include('notification.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', include('landing_page.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
