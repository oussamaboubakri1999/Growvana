# historique/views.py
from django.shortcuts import render, get_object_or_404
from .models import CultureHistorique
from rest_framework import viewsets
from .serializers import CultureHistoriqueSerializer

# API ViewSet
class CultureHistoriqueViewSet(viewsets.ModelViewSet):
    queryset = CultureHistorique.objects.all()
    serializer_class = CultureHistoriqueSerializer

# Traditional views
def historique_list(request):
    """List all historique entries"""
    historique = CultureHistorique.objects.all()
    return render(request, 'historique/list.html', {'historique': historique})

def historique_detail(request, pk):
    """Show details of one historique entry"""
    entry = get_object_or_404(CultureHistorique, pk=pk)
    return render(request, 'historique/detail.html', {'entry': entry})
