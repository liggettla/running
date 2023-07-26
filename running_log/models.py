from django.db import models
from django.contrib.auth.models import User

class Run(models.Model):
    """Model representing a run."""
    # The user who did the run. 'models.CASCADE' means that if the associated user is deleted, 
    # also delete all runs associated with that user.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The date of the run.
    date = models.DateField()

    # The distance of the run, in kilometers.
    distance = models.FloatField()

    # The total time of the run, in hh:mm:ss format.
    time = models.DurationField()

    pace = models.FloatField()  # Average pace (minutes per kilometer)

    # The __str__ method determines how the model will display in the Django admin and elsewhere
    def __str__(self):
        return f'{self.user.username} run on {self.date}'