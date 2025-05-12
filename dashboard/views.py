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
from users.models import CustomUser

@login_required
def admin_user_list(request):
    user = request.user
    if not (hasattr(user, 'role') and user.role == 'admin'):
        return redirect('dashboard:home')
    users = CustomUser.objects.all()
    return render(request, 'dashboard/admin_user_list.html', {'users': users})

@login_required
def admin_user_detail(request, user_id):
    user = request.user
    if not (hasattr(user, 'role') and user.role == 'admin'):
        return redirect('dashboard:home')
    target_user = CustomUser.objects.get(id=user_id)
    cultures = Culture.objects.filter(user=target_user)
    capteurs = Capteur.objects.filter(culture__user=target_user)
    mesures = Mesure.objects.filter(culture__user=target_user)
    alerts = Alert.objects.filter(culture__user=target_user)
    return render(request, 'dashboard/admin_user_detail.html', {
        'target_user': target_user,
        'cultures': cultures,
        'capteurs': capteurs,
        'mesures': mesures,
        'alerts': alerts,
    })

@login_required
def admin_user_cultures(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    cultures = Culture.objects.filter(user=user)
    return render(request, 'dashboard/admin_user_cultures.html', {'target_user': user, 'cultures': cultures})

@login_required
def admin_user_capteurs(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    capteurs = Capteur.objects.filter(culture__user=user)
    return render(request, 'dashboard/admin_user_capteurs.html', {'target_user': user, 'capteurs': capteurs})

@login_required
def admin_user_mesures(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    mesures = Mesure.objects.filter(culture__user=user)
    return render(request, 'dashboard/admin_user_mesures.html', {'target_user': user, 'mesures': mesures})

@login_required
def admin_user_alerts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    alerts = Alert.objects.filter(culture__user=user)
    return render(request, 'dashboard/admin_user_alerts.html', {'target_user': user, 'alerts': alerts})

from django.core.paginator import Paginator
from django.utils import timezone
import json

@login_required
def dashboard_home(request):
    """Main dashboard view showing recent activity, stats, users, and charts for admin."""
    user = request.user
    context = {}
    if hasattr(user, 'role') and user.role == 'admin':
        recent_activity = CultureHistorique.objects.order_by('-timestamp')[:10]
        latest_measurements = Mesure.objects.order_by('-timestamp')[:10]
        alerts = Alert.objects.order_by('-timestamp')[:10]
        capteurs = Capteur.objects.all()

        # User pagination
        user_list = CustomUser.objects.all().order_by('username')
        paginator = Paginator(user_list, 5)  # 5 users per page
        page_number = request.GET.get('page')
        users_page = paginator.get_page(page_number)
        context['users_page'] = users_page
        context['is_paginated'] = users_page.has_other_pages()

        # Chart data: Activities per day (last 7 days)
        today = timezone.now().date()
        activity_labels = [(today - timezone.timedelta(days=i)).strftime('%d/%m') for i in reversed(range(7))]
        activity_counts = [CultureHistorique.objects.filter(timestamp__date=(today - timezone.timedelta(days=i))).count() for i in reversed(range(7))]
        context['dashboard_activity_data'] = json.dumps({
            'labels': activity_labels,
            'counts': activity_counts
        })
        # Chart data: Alerts resolved/unresolved
        total_alerts = Alert.objects.count()
        unresolved_alerts = Alert.objects.filter(is_resolved=False).count() if hasattr(Alert, 'is_resolved') else 0
        resolved_alerts = total_alerts - unresolved_alerts
        context['dashboard_alert_data'] = json.dumps({
            'labels': ['Non résolues', 'Résolues'],
            'counts': [unresolved_alerts, resolved_alerts]
        })
        # Chart data: Measurements (last 7 days, avg per day)
        measurement_labels = [(today - timezone.timedelta(days=i)).strftime('%d/%m') for i in reversed(range(7))]
        temp_data = []
        hum_data = []
        for i in reversed(range(7)):
            day = today - timezone.timedelta(days=i)
            measures = Mesure.objects.filter(timestamp__date=day)
            temps = [m.valeur for m in measures if hasattr(m, 'type') and getattr(m, 'type', None) == 'temperature']
            hums = [m.valeur for m in measures if hasattr(m, 'type') and getattr(m, 'type', None) == 'humidity']
            temp_data.append(sum(temps)/len(temps) if temps else None)
            hum_data.append(sum(hums)/len(hums) if hums else None)
        context['dashboard_measurement_data'] = json.dumps({
            'labels': measurement_labels,
            'datasets': [
                {
                    'label': 'Température',
                    'data': temp_data,
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.1,
                },
                {
                    'label': 'Humidité',
                    'data': hum_data,
                    'borderColor': 'rgb(54, 162, 235)',
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'tension': 0.1,
                }
            ]
        })
    else:
        recent_activity = CultureHistorique.objects.filter(culture__user=user).order_by('-timestamp')[:5]
        latest_measurements = Mesure.objects.filter(culture__user=user).order_by('-timestamp')[:3]
        alerts = Alert.objects.filter(culture__user=user).order_by('-timestamp')[:5]
        capteurs = Capteur.objects.filter(culture__user=user)
        cultures = Culture.objects.filter(user=user).order_by('-id')
        context['recent_activity'] = recent_activity
        context['latest_measurements'] = latest_measurements
        context['alerts'] = alerts
        context['capteurs'] = capteurs
        context['cultures'] = cultures
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard_stats(request):
    """Dashboard statistics view."""
    user = request.user
    if hasattr(user, 'role') and user.role == 'admin':
        cultures = Culture.objects.all()
        mesures = Mesure.objects.all()
        alerts = Alert.objects.all()
        capteurs = Capteur.objects.all()
        historiques = CultureHistorique.objects.all()
    else:
        cultures = Culture.objects.filter(user=user)
        mesures = Mesure.objects.filter(culture__user=user)
        alerts = Alert.objects.filter(culture__user=user)
        capteurs = Capteur.objects.filter(culture__user=user)
        historiques = CultureHistorique.objects.filter(culture__user=user)

    total_cultures = cultures.count()
    active_cultures = 0  # adjust if you have an is_active field
    completed_cultures = 0  # adjust if you have a completed field
    total_measurements = mesures.count()
    today_measurements = mesures.filter(timestamp__gte=datetime.now() - timedelta(days=1)).count()
    avg_daily_measurements = total_measurements / (historiques.count() or 1)
    total_alerts = alerts.count()
    unresolved_alerts = alerts.filter(is_resolved=False).count()
    resolved_alerts = alerts.filter(is_resolved=True).count()
    total_capteurs = capteurs.count()
    online_capteurs = CapteurStatus.objects.filter(capteur__in=capteurs, status='online').count()
    offline_capteurs = CapteurStatus.objects.filter(capteur__in=capteurs, status='offline').count()
    # Get the latest 30 measurements, ordered by timestamp ascending (chronological)
    latest_mesures = mesures.order_by('-timestamp')[:30][::-1]
    from django.utils.dateformat import DateFormat
    dates = [DateFormat(m.timestamp).format('Y-m-d H:i') for m in latest_mesures]
    temperatures = [m.valeurs.get('temperature', None) for m in latest_mesures]
    humidities = [m.valeurs.get('humidite', None) for m in latest_mesures]

    # For demonstration, use the same data for measurement evolution as for temperature/humidity
    measurement_dates = dates
    measurement_datasets = [
        {
            'label': 'Température',
            'data': temperatures,
            'borderColor': 'rgba(34,197,94,1)',  # Green
            'backgroundColor': 'rgba(34,197,94,0.15)',  # Light green
            'pointBackgroundColor': 'rgba(34,197,94,1)',
            'pointBorderColor': 'rgba(22,163,74,1)',
            'pointRadius': 4,
            'pointHoverRadius': 7,
            'tension': 0.4,
        },
        {
            'label': 'Humidité',
            'data': humidities,
            'borderColor': 'rgba(139,92,246,1)',  # Purple
            'backgroundColor': 'rgba(139,92,246,0.13)',  # Light purple
            'pointBackgroundColor': 'rgba(139,92,246,1)',
            'pointBorderColor': 'rgba(91,33,182,1)',
            'pointRadius': 4,
            'pointHoverRadius': 7,
            'tension': 0.4,
        }
    ]

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
        'measurement_dates': json.dumps(measurement_dates),
        'measurement_datasets': json.dumps(measurement_datasets),
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
    user = request.user
    if hasattr(user, 'role') and user.role == 'admin':
        # Redirect admin to the user list dashboard
        return redirect('dashboard:admin_user_list')
    else:
        capteurs = Capteur.objects.filter(culture__user=user)
        context = {
            'capteurs': capteurs,
            'active_tab': 'devices'
        }
        return render(request, 'dashboard/devices.html', context)

@login_required
def dashboard_notifications(request):
    """User notifications view."""
    user = request.user
    if hasattr(user, 'role') and user.role == 'admin':
        alerts = Alert.objects.order_by('-timestamp')
    else:
        alerts = Alert.objects.filter(culture__user=user).order_by('-timestamp')
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
    """Create a new device. Only allow users to select their own cultures unless admin."""
    user = request.user
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        type_id = request.POST.get('type_id')
        culture_id = request.POST.get('culture_id')
        
        if identifier and type_id and culture_id:
            capteur_type = get_object_or_404(CapteurType, id=type_id)
            culture = get_object_or_404(Culture, id=culture_id)
            # Only allow assigning to user's own culture unless admin
            if hasattr(user, 'role') and user.role == 'admin' or culture.user == user:
                Capteur.objects.create(
                    identifier=identifier,
                    type=capteur_type,
                    culture=culture
                )
            return redirect(reverse('dashboard:devices'))
    capteur_types = CapteurType.objects.all()
    # Only show user's cultures unless admin
    if hasattr(user, 'role') and user.role == 'admin':
        cultures = Culture.objects.all()
    else:
        cultures = Culture.objects.filter(user=user)
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
