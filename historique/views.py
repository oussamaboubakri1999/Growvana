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
    user = request.user
    if hasattr(user, 'role') and user.role == 'admin':
        historique = CultureHistorique.objects.all()
    else:
        historique = CultureHistorique.objects.filter(culture__user=user)
    return render(request, 'historique/list.html', {'historique': historique})

def historique_detail(request, pk):
    """Show details of one historique entry"""
    entry = get_object_or_404(CultureHistorique, pk=pk)
    return render(request, 'historique/detail.html', {'entry': entry})
