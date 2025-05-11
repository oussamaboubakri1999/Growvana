from django.urls import path
from . import views

app_name = 'capteurs'

urlpatterns = [
    path('', views.capteur_list, name='capteur-list'),
    path('<int:pk>/', views.capteur_detail, name='capteur-detail'),
    path('create/', views.capteur_create, name='capteur-create'),
    path('<int:pk>/edit/', views.capteur_edit, name='capteur-edit'),
    path('capteur-form/', views.capteur_form_view, name='capteur_form'),
    path('capteur-status-form/', views.capteur_status_form_view, name='capteur_status_form'),
]
