import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GrowVana.settings')
    django.setup()

def run():
    from users.models import CustomUser
    from culture.models import Culture
    from capteurs.models import Capteur, CapteurType

    # Create a default CapteurType if none exist
    capteur_type, _ = CapteurType.objects.get_or_create(name='Température', defaults={'unit': '°C'})

    users = CustomUser.objects.exclude(username='admin_user')  # skip admin for demo
    for user in users:
        # Create a culture for each user if not exists
        culture, created = Culture.objects.get_or_create(user=user, name=f"Culture de {user.username}", defaults={'description': f'Culture test pour {user.username}'})
        if created:
            print(f"Created culture for {user.username}")
        # Create a capteur for each culture if not exists
        capteur, created = Capteur.objects.get_or_create(culture=culture, identifier=f"Capteur_{user.username}", defaults={'type': capteur_type})
        if created:
            print(f"Created capteur for {user.username}")

if __name__ == '__main__':
    setup_django()
    run()
