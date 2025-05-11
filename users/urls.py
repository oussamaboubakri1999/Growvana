from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
