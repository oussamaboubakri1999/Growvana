from django import forms
from .models import Culture

class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = ['name', 'description']
