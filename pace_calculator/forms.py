from django import forms

# this might not be needed since all forms are handled directly on the page
class PaceCalculatorForm(forms.Form):
    """Form for the Pace Calculator"""
    distance = forms.FloatField(label='Distance (in km)', required=False)
    time = forms.CharField(label='Time (hh:mm:ss)', required=False)
    pace = forms.CharField(label='Pace (hh:mm:ss)', required=False)