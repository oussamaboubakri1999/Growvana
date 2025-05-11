from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.notification_list, name='notification-list'),
    path('<int:pk>/', views.notification_detail, name='notification-detail'),
    path('create/', views.notification_create, name='notification-create'),
    path('<int:pk>/edit/', views.notification_edit, name='notification-edit'),
]
