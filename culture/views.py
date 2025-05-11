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

# Django CRUD Views
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CultureForm

def culture_list(request):
    cultures = Culture.objects.filter(user=request.user)
    return render(request, 'culture/list.html', {'cultures': cultures})

def culture_detail(request, pk):
    culture = get_object_or_404(Culture, pk=pk)
    return render(request, 'culture/detail.html', {'culture': culture})

def culture_create(request):
    user = request.user
    if request.method == 'POST':
        form = CultureForm(request.POST)
        if form.is_valid():
            culture = form.save(commit=False)
            if hasattr(user, 'role') and user.role == 'admin' and form.cleaned_data.get('user'):
                culture.user = form.cleaned_data['user']
            else:
                culture.user = user
            culture.save()
            return redirect('culture:culture-list')
    else:
        form = CultureForm()
    return render(request, 'culture/form.html', {'form': form, 'action': 'Create'})

def culture_edit(request, pk):
    culture = get_object_or_404(Culture, pk=pk)
    if request.method == 'POST':
        form = CultureForm(request.POST, instance=culture)
        if form.is_valid():
            form.save()
            return redirect('culture:culture-detail', pk=pk)
    else:
        form = CultureForm(instance=culture)
    return render(request, 'culture/form.html', {'form': form, 'action': 'Edit'})
