from django import forms
from .models import Alert


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['culture', 'message', 'is_resolved']
