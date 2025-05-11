from rest_framework import serializers
from .models import Mesure

class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = ['id', 'culture', 'capteur', 'timestamp', 'valeurs']

class MesureValueSerializer(serializers.Serializer):
    parameter = serializers.CharField()
    value = serializers.FloatField()
    timestamp = serializers.DateTimeField()
