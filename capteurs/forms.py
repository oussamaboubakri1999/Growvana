from django import forms
from .models import Capteur, CapteurStatus


class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ['identifier', 'type', 'culture']


class CapteurStatusForm(forms.ModelForm):
    class Meta:
        model = CapteurStatus
        fields = ['status']
