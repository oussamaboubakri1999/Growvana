from django.urls import path
from . import views

app_name = 'culture'

urlpatterns = [
    path('', views.culture_list, name='culture-list'),
    path('<int:pk>/', views.culture_detail, name='culture-detail'),
    path('create/', views.culture_create, name='culture-create'),
    path('<int:pk>/edit/', views.culture_edit, name='culture-edit'),
]
