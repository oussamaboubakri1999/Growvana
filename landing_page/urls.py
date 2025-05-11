from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'landing_page'

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
