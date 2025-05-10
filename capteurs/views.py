# capteurs/views.py
from rest_framework import viewsets
from .models import Capteur, CapteurType, CapteurStatus
from .serializers import CapteurSerializer, CapteurTypeSerializer, CapteurStatusSerializer

class CapteurViewSet(viewsets.ModelViewSet):
    queryset = Capteur.objects.all()
    serializer_class = CapteurSerializer

class CapteurTypeViewSet(viewsets.ModelViewSet):
    queryset = CapteurType.objects.all()
    serializer_class = CapteurTypeSerializer

class CapteurStatusViewSet(viewsets.ModelViewSet):
    queryset = CapteurStatus.objects.all()
    serializer_class = CapteurStatusSerializer
