from django.urls import path
from . import views

app_name = 'mesures'

urlpatterns = [
    path('', views.mesure_list, name='mesure-list'),
    path('<int:pk>/', views.mesure_detail, name='mesure-detail'),
    path('create/', views.mesure_create, name='mesure-create'),
    path('<int:pk>/edit/', views.mesure_edit, name='mesure-edit'),
]
