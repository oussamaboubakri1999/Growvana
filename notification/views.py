# notifications/views.py
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alert
from .serializers import AlertSerializer
from .forms import AlertForm


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


def notification_list(request):
    alerts = Alert.objects.all().order_by('-timestamp')
    return render(request, 'notification/list.html', {'alerts': alerts})


def notification_detail(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    return render(request, 'notification/detail.html', {'alert': alert})


def notification_create(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notification:notification-list')
    else:
        form = AlertForm()
    return render(request, 'notification/form.html', {'form': form, 'action': 'Create'})


def notification_edit(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    if request.method == 'POST':
        form = AlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('notification:notification-detail', pk=pk)
    else:
        form = AlertForm(instance=alert)
    return render(request, 'notification/form.html', {'form': form, 'action': 'Edit'})
