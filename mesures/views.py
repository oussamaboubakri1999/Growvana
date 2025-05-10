# mesures/views.py
from rest_framework import viewsets
from .models import Mesure
from .serializers import MesureSerializer

class MesureViewSet(viewsets.ModelViewSet):
    queryset = Mesure.objects.all()
    serializer_class = MesureSerializer
