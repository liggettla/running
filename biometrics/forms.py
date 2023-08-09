from django import forms
from .models import Biometric

class BiometricForm(forms.ModelForm):
    class Meta:
        model = Biometric
        fields = [
            'weight_morning',
            'weight_after_run',
            'weight_night',
            'heart_rate',
            'systolic_pressure',
            'diastolic_pressure'
            ]
