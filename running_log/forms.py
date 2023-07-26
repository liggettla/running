from django import forms
from .models import Run

class RunForm(forms.ModelForm):
    """Form for adding a run."""
    class Meta:
        # The model this form is associated with.
        model = Run

        # The fields to include in the form. These should be the same as the fields in the model,
        # except for 'user' because the user will be automatically determined based on who is logged in.
        fields = ['date', 'distance', 'time', 'pace']