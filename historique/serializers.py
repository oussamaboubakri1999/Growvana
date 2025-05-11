from rest_framework import serializers
from .models import CultureHistorique

class CultureHistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureHistorique
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')
