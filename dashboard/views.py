from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from historique.models import CultureHistorique, Culture
from mesures.models import Mesure
from notification.models import Alert
from capteurs.models import Capteur, CapteurStatus, CapteurType
from datetime import datetime, timedelta
import json

# Remove unused Device import
# from capteurs.models import Device

# Create your views here.

@login_required
def dashboard_home(request):
    """Main dashboard view showing recent activity and stats."""
    recent_activity = CultureHistorique.objects.order_by('-timestamp')[:5]
    latest_measurements = Mesure.objects.order_by('-timestamp')[:3]
    alerts = Alert.objects.order_by('-timestamp')[:5]
    capteurs = Capteur.objects.all()

    context = {
        'recent_activity': recent_activity,
        'latest_measurements': latest_measurements,
        'alerts': alerts,
        'capteurs': capteurs,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard_stats(request):
    """Dashboard statistics view."""
    # Culture statistics
    total_cultures = Culture.objects.count()
    # No is_active field on Culture; set dummy values or remove these lines
    active_cultures = 0
    completed_cultures = 0

    # Measurement statistics
    total_measurements = Mesure.objects.count()
    today_measurements = Mesure.objects.filter(
        timestamp__gte=datetime.now() - timedelta(days=1)
    ).count()
    avg_daily_measurements = total_measurements / (CultureHistorique.objects.count() or 1)

    # Alert statistics
    total_alerts = Alert.objects.count()
    unresolved_alerts = Alert.objects.filter(is_resolved=False).count()
    resolved_alerts = Alert.objects.filter(is_resolved=True).count()

    # Device statistics
    total_capteurs = Capteur.objects.count()
    online_capteurs = CapteurStatus.objects.filter(status='online').count()
    offline_capteurs = CapteurStatus.objects.filter(status='offline').count()

    # Chart data
    measurements = Mesure.objects.order_by('timestamp')[:30]
    dates = [m.timestamp.strftime('%Y-%m-%d %H:%M') for m in measurements]
    temperatures = [m.valeurs.get('temperature', 0) for m in measurements]
    humidities = [m.valeurs.get('humidity', 0) for m in measurements]

    context = {
        'total_cultures': total_cultures,
        'active_cultures': active_cultures,
        'completed_cultures': completed_cultures,
        'total_measurements': total_measurements,
        'today_measurements': today_measurements,
        'avg_daily_measurements': round(avg_daily_measurements, 2),
        'total_alerts': total_alerts,
        'unresolved_alerts': unresolved_alerts,
        'resolved_alerts': resolved_alerts,
        'total_capteurs': total_capteurs,
        'online_capteurs': online_capteurs,
        'offline_capteurs': offline_capteurs,
        'dates': json.dumps(dates),
        'temperatures': json.dumps(temperatures),
        'humidities': json.dumps(humidities),
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
    capteurs = Capteur.objects.all()
    context = {
        'capteurs': capteurs,
        'active_tab': 'devices'
    }
    return render(request, 'dashboard/devices.html', context)

@login_required
def dashboard_notifications(request):
    """User notifications view."""
    alerts = Alert.objects.order_by('-timestamp')
    context = {
        'alerts': alerts,
        'active_tab': 'notifications'
    }
    return render(request, 'dashboard/notifications.html', context)

@login_required
def notifications_create(request):
    """Create a new notification."""
    if request.method == 'POST':
        culture_id = request.POST.get('culture_id')
        message = request.POST.get('message')
        
        if culture_id and message:
            culture = get_object_or_404(Culture, id=culture_id)
            Alert.objects.create(culture=culture, message=message)
            return redirect(reverse('dashboard:notifications'))
    
    cultures = Culture.objects.all()
    context = {
        'cultures': cultures,
        'active_tab': 'notifications'
    }
    return render(request, 'dashboard/notifications_form.html', context)

@login_required
def notifications_detail(request, alert_id):
    """View notification details."""
    alert = get_object_or_404(Alert, id=alert_id)
    context = {
        'alert': alert,
        'active_tab': 'notifications'
    }
    return render(request, 'dashboard/notifications_detail.html', context)

@login_required
def notifications_delete(request, alert_id):
    """Delete a notification."""
    alert = get_object_or_404(Alert, id=alert_id)
    alert.delete()
    return redirect(reverse('dashboard:notifications'))

@login_required
def devices_create(request):
    """Create a new device."""
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        type_id = request.POST.get('type_id')
        culture_id = request.POST.get('culture_id')
        
        if identifier and type_id and culture_id:
            capteur_type = get_object_or_404(CapteurType, id=type_id)
            culture = get_object_or_404(Culture, id=culture_id)
            Capteur.objects.create(
                identifier=identifier,
                type=capteur_type,
                culture=culture
            )
            return redirect(reverse('dashboard:devices'))
    
    capteur_types = CapteurType.objects.all()
    cultures = Culture.objects.all()
    context = {
        'capteur_types': capteur_types,
        'cultures': cultures,
        'active_tab': 'devices'
    }
    return render(request, 'dashboard/devices_form.html', context)

@login_required
def devices_detail(request, capteur_id):
    """View device details."""
    capteur = get_object_or_404(Capteur, id=capteur_id)
    context = {
        'capteur': capteur,
        'active_tab': 'devices'
    }
    return render(request, 'dashboard/devices_detail.html', context)

@login_required
def devices_delete(request, capteur_id):
    """Delete a device."""
    capteur = get_object_or_404(Capteur, id=capteur_id)
    capteur.delete()
    return redirect(reverse('dashboard:devices'))

@login_required
def devices_update_status(request, capteur_id):
    """Update device status."""
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['online', 'offline']:
            capteur = get_object_or_404(Capteur, id=capteur_id)
            CapteurStatus.objects.create(
                capteur=capteur,
                status=status
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
