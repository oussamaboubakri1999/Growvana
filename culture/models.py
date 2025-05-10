# cultures/models.py
from django.db import models

class Culture(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CultureThreshold(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='thresholds')
    metric = models.CharField(max_length=50)  # e.g. "temperature"
    min_value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return f"{self.metric} thresholds for {self.culture.name}"
