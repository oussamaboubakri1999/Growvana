# capteurs/views.py
from rest_framework import viewsets
from .models import Capteur, CapteurType, CapteurStatus
from .serializers import CapteurSerializer, CapteurTypeSerializer, CapteurStatusSerializer

# DRF API ViewSets
class CapteurViewSet(viewsets.ModelViewSet):
    queryset = Capteur.objects.all()
    serializer_class = CapteurSerializer

class CapteurTypeViewSet(viewsets.ModelViewSet):
    queryset = CapteurType.objects.all()
    serializer_class = CapteurTypeSerializer

class CapteurStatusViewSet(viewsets.ModelViewSet):
    queryset = CapteurStatus.objects.all()
    serializer_class = CapteurStatusSerializer

# Django CRUD Views
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CapteurForm, CapteurStatusForm

def capteur_list(request):
    capteurs = Capteur.objects.all()
    return render(request, 'capteurs/list.html', {'capteurs': capteurs})

def capteur_detail(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    return render(request, 'capteurs/detail.html', {'capteur': capteur})

def capteur_create(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('capteurs:capteur-list')
    else:
        form = CapteurForm()
    return render(request, 'capteurs/form.html', {'form': form, 'action': 'Create'})

def capteur_edit(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    if request.method == 'POST':
        form = CapteurForm(request.POST, instance=capteur)
        if form.is_valid():
            form.save()
            return redirect('capteurs:capteur-detail', pk=pk)
    else:
        form = CapteurForm(instance=capteur)
    return render(request, 'capteurs/form.html', {'form': form, 'action': 'Edit'})

def capteur_form_view(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('capteur_form')
    else:
        form = CapteurForm()
    return render(request, 'capteurs/capteur_form.html', {'form': form})

def capteur_status_form_view(request):
    if request.method == 'POST':
        form = CapteurStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('capteur_status_form')
    else:
        form = CapteurStatusForm()
    return render(request, 'capteurs/capteur_status_form.html', {'form': form})
