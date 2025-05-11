from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from historique.models import Historique
from mesures.models import Mesure
from notification.models import Notification
from capteurs.models import Device

# Create your views here.

@login_required
def dashboard_home(request):
    """Main dashboard view showing recent activity and stats."""
    recent_activity = Historique.objects.filter(user=request.user).order_by('-date')[:5]
    latest_measurements = Mesure.objects.filter(user=request.user).order_by('-date')[:3]
    
    context = {
        'recent_activity': recent_activity,
        'latest_measurements': latest_measurements,
        'active_tab': 'home'
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard_stats(request):
    """Dashboard statistics view with charts and analytics."""
    measurements = Mesure.objects.filter(user=request.user).order_by('date')
    
    context = {
        'measurements': measurements,
        'active_tab': 'stats'
    }
    return render(request, 'dashboard/stats.html', context)

@login_required
def dashboard_settings(request):
    """User settings view."""
    context = {
        'active_tab': 'settings',
        'user': request.user
    }
    return render(request, 'dashboard/settings.html', context)

@login_required
def dashboard_devices(request):
    """Connected devices management view."""
    devices = Device.objects.filter(user=request.user)
    
    context = {
        'active_tab': 'devices',
        'devices': devices
    }
    return render(request, 'dashboard/devices.html', context)

@login_required
def dashboard_notifications(request):
    """User notifications view."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'active_tab': 'notifications',
        'notifications': notifications
    }
    return render(request, 'dashboard/notifications.html', context)
