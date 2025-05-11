import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import CustomUser
from culture.models import Culture, CultureThreshold
from capteurs.models import Capteur, CapteurType, CapteurStatus
from notification.models import Alert
from mesures.models import Mesure

User = CustomUser

# Capteur types for metrics
CAPTEUR_TYPES = [
    {"name": "Température", "unit": "°C", "metric": "temperature"},
    {"name": "Humidité", "unit": "%", "metric": "humidite"},
    {"name": "pH", "unit": "", "metric": "ph"},
    {"name": "Niveau d'eau", "unit": "L", "metric": "niveau_eau"},
    {"name": "CO2", "unit": "ppm", "metric": "co2"},
    {"name": "Lumière", "unit": "lux", "metric": "lumiere"},
]

class Command(BaseCommand):
    help = "Populate the database with dummy data for all main models."

    def handle(self, *args, **options):
        # 1. Users
        users = [
            {"username": "admin", "email": "admin@growvana.com", "password": "adminpass", "role": "admin"},
            {"username": "operator1", "email": "operator1@growvana.com", "password": "operatorpass1", "role": "operator"},
            {"username": "operator2", "email": "operator2@growvana.com", "password": "operatorpass2", "role": "operator"},
            {"username": "viewer1", "email": "viewer1@growvana.com", "password": "viewerpass1", "role": "viewer"},
            {"username": "viewer2", "email": "viewer2@growvana.com", "password": "viewerpass2", "role": "viewer"},
        ]
        for u in users:
            user, created = User.objects.get_or_create(username=u["username"], defaults={
                "email": u["email"], "role": u["role"]
            })
            if created:
                user.set_password(u["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username} ({user.role})"))
            else:
                # Update role/email if needed
                updated = False
                if user.role != u["role"]:
                    user.role = u["role"]
                    updated = True
                if user.email != u["email"]:
                    user.email = u["email"]
                    updated = True
                if updated:
                    user.save()
                self.stdout.write(f"User already exists: {user.username}")

        # 2. CapteurTypes
        type_objs = {}
        for t in CAPTEUR_TYPES:
            obj, created = CapteurType.objects.get_or_create(name=t["name"], defaults={"unit": t["unit"]})
            type_objs[t["metric"]] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created CapteurType: {obj.name}"))
            else:
                self.stdout.write(f"CapteurType already exists: {obj.name}")

        # 3. For each Culture
        all_cultures = Culture.objects.all()
        for culture in all_cultures:
            # 3.1 Capteurs
            capteurs = []
            for i in range(1, random.randint(2, 4)):
                metric = random.choice(list(type_objs.keys()))
                identifier = f"{culture.name[:3].lower()}-c{i}-{metric}"
                capteur, created = Capteur.objects.get_or_create(
                    identifier=identifier,
                    defaults={
                        "type": type_objs[metric],
                        "culture": culture
                    }
                )
                capteurs.append(capteur)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Capteur: {capteur.identifier}"))
                else:
                    self.stdout.write(f"Capteur already exists: {capteur.identifier}")
                # 3.2 CapteurStatus
                status, st_created = CapteurStatus.objects.get_or_create(
                    capteur=capteur,
                    defaults={
                        "last_seen": timezone.now() - timedelta(minutes=random.randint(0, 120)),
                        "status": random.choice(["online", "offline"])
                    }
                )
                if st_created:
                    self.stdout.write(self.style.SUCCESS(f"  Added status for {capteur.identifier}"))
                else:
                    self.stdout.write(f"  Status already exists for {capteur.identifier}")

                # 3.3 Mesures (10 per capteur)
                thresholds = {th.metric: (th.min_value, th.max_value) for th in culture.thresholds.all()}
                for j in range(10):
                    valeurs = {}
                    for metric, (minv, maxv) in thresholds.items():
                        # Random value within threshold
                        valeurs[metric] = round(random.uniform(minv, maxv), 2)
                    Mesure.objects.create(
                        culture=culture,
                        valeurs=valeurs,
                        timestamp=timezone.now() - timedelta(days=random.randint(0, 10), hours=random.randint(0, 23))
                    )
                self.stdout.write(self.style.SUCCESS(f"  Added 10 mesures for {capteur.identifier}"))

            # 3.4 Alerts (1-2 per culture)
            for a in range(random.randint(1, 2)):
                Alert.objects.create(
                    culture=culture,
                    message=f"Alerte dummy pour {culture.name}: seuil dépassé sur {random.choice(list(type_objs.keys()))}",
                    is_resolved=random.choice([True, False]),
                    timestamp=timezone.now() - timedelta(days=random.randint(0, 5))
                )
            self.stdout.write(self.style.SUCCESS(f"Added alerts for {culture.name}"))

        self.stdout.write(self.style.SUCCESS("Dummy data for all models populated!"))
