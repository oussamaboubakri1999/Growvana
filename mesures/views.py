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
    mesures = Mesure.objects.filter(culture__user=request.user)
    return render(request, 'mesures/list.html', {'mesures': mesures})

def mesure_detail(request, pk):
    mesure = get_object_or_404(Mesure, pk=pk)
    return render(request, 'mesures/detail.html', {'mesure': mesure})

def mesure_create(request):
    user = request.user
    if hasattr(user, 'role') and user.role == 'admin':
        cultures = Culture.objects.all()
    else:
        cultures = Culture.objects.filter(user=user)
    if request.method == 'POST':
        form = MesureForm(request.POST)
        form.fields['culture'].queryset = cultures
        if form.is_valid():
            mesure = form.save(commit=False)
            if not (hasattr(user, 'role') and user.role == 'admin'):
                mesure.culture = form.cleaned_data['culture']
            mesure.save()
            return redirect('mesures:mesure-list')
    else:
        form = MesureForm()
        form.fields['culture'].queryset = cultures
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
