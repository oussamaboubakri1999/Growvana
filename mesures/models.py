# mesures/models.py
from django.db import models
from culture.models import Culture

class Mesure(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='mesures')
    timestamp = models.DateTimeField(auto_now_add=True)
    valeurs = models.JSONField()  # e.g. {"temperature": 25, "ph": 7.1, "humidite": 60}

    def __str__(self):
        return f"{self.culture.name} @ {self.timestamp}"
