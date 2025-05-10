from django.shortcuts import render

# Create your views here.

def dashboard_home(request):
    return render(request, 'dashboard/home.html')

def dashboard_stats(request):
    return render(request, 'dashboard/stats.html')
