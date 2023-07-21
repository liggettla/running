from django import forms

class PaceCalculatorForm(forms.Form):
    """Form for the Pace Calculator"""
    distance = forms.FloatField(label='Distance (in km)', required=False)
    time = forms.CharField(label='Time (hh:mm:ss)', required=False)
    pace = forms.CharField(label='Pace (hh:mm:ss)', required=False)