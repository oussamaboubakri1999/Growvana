import random
from django.core.management.base import BaseCommand
from culture.models import Culture, CultureThreshold

PLANTES_DATA = [
    {
        "nom": "menthe",
        "temperature": (18, 24),
        "humidite": (50, 70),
        "ph": (6.0, 7.5),
        "niveau_eau": (5, 10),
        "co2": (300, 800),
        "lumiere": (15000, 25000)
    },
    {
        "nom": "laitue",
        "temperature": (16, 22),
        "humidite": (60, 80),
        "ph": (6.0, 7.0),
        "niveau_eau": (4, 8),
        "co2": (250, 800),
        "lumiere": (12000, 20000)
    },
    {
        "nom": "epinard",
        "temperature": (10, 20),
        "humidite": (60, 70),
        "ph": (6.2, 7.5),
        "niveau_eau": (6, 10),
        "co2": (300, 700),
        "lumiere": (14000, 22000)
    },
    {
        "nom": "basilic",
        "temperature": (20, 27),
        "humidite": (50, 70),
        "ph": (5.5, 6.5),
        "niveau_eau": (5, 9),
        "co2": (300, 800),
        "lumiere": (15000, 25000)
    },
    {
        "nom": "comcombre",
        "temperature": (22, 28),
        "humidite": (60, 80),
        "ph": (5.5, 6.8),
        "niveau_eau": (6, 10),
        "co2": (350, 900),
        "lumiere": (18000, 26000)
    },
    {
        "nom": "fraise",
        "temperature": (18, 24),
        "humidite": (70, 80),
        "ph": (5.8, 6.5),
        "niveau_eau": (6, 9),
        "co2": (300, 850),
        "lumiere": (16000, 25000)
    },
    {
        "nom": "tomate",
        "temperature": (20, 26),
        "humidite": (60, 75),
        "ph": (5.5, 6.8),
        "niveau_eau": (5, 9),
        "co2": (350, 900),
        "lumiere": (18000, 26000)
    },
    {
        "nom": "pomme de terre",
        "temperature": (15, 22),
        "humidite": (60, 70),
        "ph": (5.0, 6.0),
        "niveau_eau": (4, 8),
        "co2": (300, 800),
        "lumiere": (12000, 20000)
    },
    {
        "nom": "ognion",
        "temperature": (13, 24),
        "humidite": (55, 70),
        "ph": (6.0, 7.0),
        "niveau_eau": (5, 8),
        "co2": (250, 750),
        "lumiere": (12000, 18000)
    }
]

METRIC_MAP = {
    "temperature": "Température (°C)",
    "humidite": "Humidité (%)",
    "ph": "pH",
    "niveau_eau": "Niveau d'eau (L)",
    "co2": "CO2 (ppm)",
    "lumiere": "Lumière (lux)"
}

class Command(BaseCommand):
    help = "Populate the database with dummy plant cultures and thresholds."

    def handle(self, *args, **options):
        for plante in PLANTES_DATA:
            culture, created = Culture.objects.get_or_create(
                name=plante["nom"],
                defaults={"description": f"Culture de {plante['nom']} (donnée de test)"}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created culture: {culture.name}"))
            else:
                self.stdout.write(f"Culture already exists: {culture.name}")
            # Add thresholds
            for metric_key, metric_label in METRIC_MAP.items():
                min_val, max_val = plante[metric_key]
                threshold, t_created = CultureThreshold.objects.get_or_create(
                    culture=culture,
                    metric=metric_key,
                    defaults={
                        "min_value": min_val,
                        "max_value": max_val
                    }
                )
                if t_created:
                    self.stdout.write(self.style.SUCCESS(f"  Added threshold for {metric_key}: {min_val}-{max_val}"))
                else:
                    self.stdout.write(f"  Threshold already exists for {metric_key} in {culture.name}")
        self.stdout.write(self.style.SUCCESS("Dummy plant data population complete!"))
