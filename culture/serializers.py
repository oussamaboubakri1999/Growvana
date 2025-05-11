from rest_framework import serializers
from .models import Culture, CultureThreshold

class CultureThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureThreshold
        fields = ['id', 'culture', 'parameter', 'min_value', 'max_value']

class CultureSerializer(serializers.ModelSerializer):
    thresholds = CultureThresholdSerializer(many=True, read_only=True)
    
    class Meta:
        model = Culture
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'thresholds']
