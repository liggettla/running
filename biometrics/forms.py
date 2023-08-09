from django import forms
from .models import Biometric

class BiometricForm(forms.ModelForm):
    # create a date field that uses the HTML5 date input datepicker type
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Biometric
        fields = [
            'date',
            'weight_morning',
            'weight_after_run',
            'weight_night',
            'heart_rate',
            'systolic_pressure',
            'diastolic_pressure'
            ]