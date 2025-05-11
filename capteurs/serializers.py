from rest_framework import serializers
from .models import Capteur, CapteurType, CapteurStatus

class CapteurTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapteurType
        fields = ['id', 'name', 'description']

class CapteurStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapteurStatus
        fields = ['id', 'capteur', 'status', 'timestamp']

class CapteurSerializer(serializers.ModelSerializer):
    type = CapteurTypeSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Capteur
        fields = ['id', 'identifier', 'type', 'culture', 'status']
        
    def get_status(self, obj):
        latest_status = obj.capteurstatus_set.order_by('-timestamp').first()
        return {
            'status': latest_status.status if latest_status else 'offline',
            'timestamp': latest_status.timestamp if latest_status else None
        }
