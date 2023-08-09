from django.db import models
from django.contrib.auth.models import User

class Biometric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # blank=False means that the field is required
    date = models.DateField(auto_now_add=False, blank=False)

    # Weight fields
    weight_morning = models.FloatField(null=True, blank=True)
    weight_after_run = models.FloatField(null=True, blank=True)
    weight_night = models.FloatField(null=True, blank=True)

    # Heart rate and blood pressure
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    systolic_pressure = models.PositiveIntegerField(null=True, blank=True)  # Upper number
    diastolic_pressure = models.PositiveIntegerField(null=True, blank=True)  # Lower number

    def __str__(self):
        return f"{self.user.username}'s biometrics on {self.date}"
