from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def landing_page(request):
    """Render the landing page with service information."""
    services = [
        {'name': 'Monitoring', 'description': 'Real-time plant monitoring', 'icon': 'tachometer-alt'},
        {'name': 'Automation', 'description': 'Smart irrigation control', 'icon': 'robot'},
        {'name': 'Analytics', 'description': 'Growth analytics & reports', 'icon': 'chart-line'}
    ]
    return render(request, 'landing_page/index.html', {'services': services})

def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('landing_page:login')
    else:
        form = UserCreationForm()
    return render(request, 'landing_page/register.html', {'form': form})

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'landing_page/login.html')
