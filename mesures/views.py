# mesures/views.py
from rest_framework import viewsets
from .models import Mesure
from .serializers import MesureSerializer

class MesureViewSet(viewsets.ModelViewSet):
    queryset = Mesure.objects.all()
    serializer_class = MesureSerializer

# Django CRUD Views
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MesureForm

def mesure_list(request):
    mesures = Mesure.objects.all()
    return render(request, 'mesures/list.html', {'mesures': mesures})

def mesure_detail(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    return render(request, 'mesures/detail.html', {'mesure': mesure})

def mesure_create(request):
    if request.method == 'POST':
        form = MesureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mesures:mesure-list')
    else:
        form = MesureForm()
    return render(request, 'mesures/form.html', {'form': form, 'action': 'Create'})

def mesure_edit(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    if request.method == 'POST':
        form = MesureForm(request.POST, instance=mesure)
        if form.is_valid():
            form.save()
            return redirect('mesures:mesure-detail', pk=pk)
    else:
        form = MesureForm(instance=mesure)
    return render(request, 'mesures/form.html', {'form': form, 'action': 'Edit'})
