# cultures/views.py
from rest_framework import viewsets
from .models import Culture, CultureThreshold
from .serializers import CultureSerializer, CultureThresholdSerializer

class CultureViewSet(viewsets.ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer

class CultureThresholdViewSet(viewsets.ModelViewSet):
    queryset = CultureThreshold.objects.all()
    serializer_class = CultureThresholdSerializer
