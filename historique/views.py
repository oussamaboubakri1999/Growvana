# historique/views.py
from rest_framework import viewsets
from .models import CultureHistorique
from .serializers import CultureHistoriqueSerializer

class CultureHistoriqueViewSet(viewsets.ModelViewSet):
    queryset = CultureHistorique.objects.all()
    serializer_class = CultureHistoriqueSerializer
