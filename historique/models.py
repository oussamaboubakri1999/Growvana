# historique/models.py
from django.db import models
from culture.models import Culture

class CultureHistorique(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='historique')
    timestamp = models.DateTimeField()
    temperature = models.FloatField(null=True, blank=True)
    humidite = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    co2 = models.FloatField(null=True, blank=True)
    niveau_eau = models.FloatField(null=True, blank=True)
    lumiere = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Historique {self.culture.name} @ {self.timestamp}"
