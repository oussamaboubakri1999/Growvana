# notifications/models.py
from django.db import models
from culture.models import Culture

class Alert(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert on {self.culture.name} at {self.timestamp}"
