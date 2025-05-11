from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'landing_page'

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]
