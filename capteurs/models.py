# capteurs/models.py
from django.db import models
from culture.models import Culture

class CapteurType(models.Model):
    name = models.CharField(max_length=50)  # e.g. Temperature, pH, etc.
    unit = models.CharField(max_length=20)  # °C, %, etc.

    def __str__(self):
        return self.name

class Capteur(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(CapteurType, on_delete=models.CASCADE)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='capteurs')

    def __str__(self):
        return self.identifier

class CapteurStatus(models.Model):
    capteur = models.OneToOneField(Capteur, on_delete=models.CASCADE)
    last_seen = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('online', 'Online'), ('offline', 'Offline')])

    def __str__(self):
        return f"{self.capteur.identifier} is {self.status}"
 