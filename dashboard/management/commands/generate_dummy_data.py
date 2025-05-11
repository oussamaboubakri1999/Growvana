from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from culture.models import Culture, CultureThreshold
from capteurs.models import CapteurType, Capteur, CapteurStatus
from historique.models import CultureHistorique
from mesures.models import Mesure
from notification.models import Alert
import random

class Command(BaseCommand):
    help = 'Generate dummy data for all models (except plants)'

    def handle(self, *args, **kwargs):
        # Users
        import csv
        users = []
        user_rows = []
        # Create 1 admin
        admin, _ = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.set_password('test1234')
        admin.save()
        users.append(admin)
        user_rows.append({'username': admin.username, 'email': admin.email, 'password': 'test1234'})
        # Create 5 operators
        for i in range(5):
            op_username = f'operator_user{i+1}'
            op_email = f'operator{i+1}@example.com'
            operator, _ = User.objects.get_or_create(
                username=op_username,
                defaults={
                    'email': op_email,
                    'role': 'operator',
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            operator.set_password('test1234')
            operator.save()
            users.append(operator)
            user_rows.append({'username': operator.username, 'email': operator.email, 'password': 'test1234'})
        # Create 1 viewer
        viewer, _ = User.objects.get_or_create(
            username='viewer_user',
            defaults={
                'email': 'viewer@example.com',
                'role': 'viewer',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        viewer.set_password('test1234')
        viewer.save()
        users.append(viewer)
        user_rows.append({'username': viewer.username, 'email': viewer.email, 'password': 'test1234'})

        # Write users to CSV
        with open('users_dummy.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['username', 'email', 'password'])
            writer.writeheader()
            for row in user_rows:
                writer.writerow(row)
        self.stdout.write(self.style.SUCCESS('Users created and exported to users_dummy.csv.'))

        # Cultures: 2 per operator
        cultures = []
        for operator in users:
            if hasattr(operator, 'role') and operator.role == 'operator':
                for j in range(2):
                    culture, _ = Culture.objects.get_or_create(
                        name=f'Culture_{operator.username}_{j+1}',
                        user=operator,
                        defaults={'description': f'Description for {operator.username} culture {j+1}'}
                    )
                    cultures.append(culture)
        self.stdout.write(self.style.SUCCESS('Cultures created.'))

        # CultureThresholds
        metrics = ["temperature", "humidite", "ph", "co2", "niveau_eau", "lumiere"]
        for culture in cultures:
            for metric in metrics:
                CultureThreshold.objects.get_or_create(
                    culture=culture,
                    metric=metric,
                    defaults={
                        'min_value': random.uniform(10, 20),
                        'max_value': random.uniform(21, 35)
                    }
                )
        self.stdout.write(self.style.SUCCESS('Culture thresholds created.'))

        # CapteurTypes
        types = [
            ("Temperature", "°C"),
            ("Humidite", "%"),
            ("pH", "pH"),
            ("CO2", "ppm"),
            ("Niveau Eau", "L"),
            ("Lumiere", "lux")
        ]
        capteur_types = []
        for name, unit in types:
            ct, _ = CapteurType.objects.get_or_create(name=name, unit=unit)
            capteur_types.append(ct)
        self.stdout.write(self.style.SUCCESS('Capteur types created.'))

        # Capteurs
        capteurs = []
        for culture in cultures:
            for ct in capteur_types:
                identifier = f'{ct.name.lower()}_{culture.pk}'
                capteur, _ = Capteur.objects.get_or_create(
                    identifier=identifier,
                    type=ct,
                    culture=culture
                )
                capteurs.append(capteur)
        self.stdout.write(self.style.SUCCESS('Capteurs created.'))

        # CapteurStatus
        for capteur in capteurs:
            CapteurStatus.objects.get_or_create(
                capteur=capteur,
                defaults={
                    'last_seen': timezone.now(),
                    'status': random.choice(['online', 'offline'])
                }
            )
        self.stdout.write(self.style.SUCCESS('Capteur statuses created.'))

        # Historique
        for culture in cultures:
            for _ in range(5):
                CultureHistorique.objects.create(
                    culture=culture,
                    timestamp=timezone.now() - timezone.timedelta(days=random.randint(0,10)),
                    temperature=random.uniform(15, 30),
                    humidite=random.uniform(30, 80),
                    ph=random.uniform(5.5, 8),
                    co2=random.uniform(300, 1000),
                    niveau_eau=random.uniform(10, 50),
                    lumiere=random.uniform(100, 1000)
                )
        self.stdout.write(self.style.SUCCESS('Historique created.'))

        # Mesures
        for culture in cultures:
            for _ in range(5):
                Mesure.objects.create(
                    culture=culture,
                    valeurs={
                        'temperature': random.uniform(15, 30),
                        'ph': random.uniform(5.5, 8),
                        'humidite': random.uniform(30, 80),
                        'co2': random.uniform(300, 1000),
                        'niveau_eau': random.uniform(10, 50),
                        'lumiere': random.uniform(100, 1000)
                    }
                )
        self.stdout.write(self.style.SUCCESS('Mesures created.'))

        # Alerts
        for culture in cultures:
            for _ in range(3):
                Alert.objects.create(
                    culture=culture,
                    message=f"Dummy alert for {culture.name}",
                    is_resolved=random.choice([True, False])
                )
        self.stdout.write(self.style.SUCCESS('Alerts created.'))

        self.stdout.write(self.style.SUCCESS('Dummy data generation complete!'))
