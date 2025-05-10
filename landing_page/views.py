from django.shortcuts import render

def landing_page(request):
    services = [
        {'name': 'Monitoring', 'description': 'Real-time plant monitoring'},
        {'name': 'Automation', 'description': 'Smart irrigation control'},
        {'name': 'Analytics', 'description': 'Growth analytics & reports'}
    ]
    products = [
        {'name': 'Smart Sensor Kit', 'description': 'Set of 5 sensors'},
        {'name': 'Control Hub', 'description': 'Central control unit'},
        {'name': 'Mobile App', 'description': 'iOS & Android app'}
    ]
    return render(request, 'landing_page/index.html', {'services': services, 'products': products})
