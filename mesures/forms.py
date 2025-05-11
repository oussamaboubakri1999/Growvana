from django import forms
from .models import Mesure

class MesureForm(forms.ModelForm):
    class Meta:
        model = Mesure
        fields = ['culture', 'valeurs']
