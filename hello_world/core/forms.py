from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# This inherits from UserCreationForm, which is a built-in
# form for creating new users included in Django
class NewUserForm(UserCreationForm):
    # Add an email field to the form
    email = forms.EmailField(required=True)

    class Meta:
        model = User # Use the built-in User model
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False) # Call the built-in save() method
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user