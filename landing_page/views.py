from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

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
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is verified
            user.save()

            # Send verification email
            subject = 'Verify your email for GrowVana'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verification_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')
            message = render_to_string('registration/verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, 'Please check your email to verify your account.')
            return redirect('landing_page:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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

def verify_email(request, uidb64, token):
    """Handle email verification."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('landing_page:login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('landing_page:register')
