from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('dashboard', RedirectView.as_view(url='/dashboard/')),  # Redirect non-trailing to trailing slash
    path('', include(('landing_page.urls', 'landing_page'), namespace='landing_page')),
    path('api/historique/', include('historique.urls', namespace='historique')),
    path('accounts/', include('allauth.urls')),
]
