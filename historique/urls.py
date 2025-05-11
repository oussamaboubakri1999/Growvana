from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'culture-historique', views.CultureHistoriqueViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Traditional views
    path('', views.historique_list, name='historique-list'),
    path('<int:pk>/', views.historique_detail, name='historique-detail'),
]
