from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    SEX_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
        ("N", "Not Specified")
    ]

    age = models.IntegerField(default=0)
    sex = models.CharField(default="N", max_length=1, choices=SEX_OPTIONS)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)

class WorkoutHistory(models.Model):
    pass
    # user = models.ForeignKey()
    # session_name = models.CharField()
    # date = models.DateField()

class Sessions(models.Model):
    pass
    # session = models.ForeignKey()
    # exercise = models.ForeignKey()
    # sets = models.IntegerField()
    # weight = models.FloatField()
    # kgorlb = models.CharField()
    # reps = models.IntegerField()
    # time = models.TimeField()
    # pace = models.TimeField()
    # distance = models.FloatField()
    # kmormiles = models.CharField()
    # notes = models.CharField()
    # session_duration = models.TimeField()

class ExerciseList(models.Model):
    pass
    # exercise_name = models.CharField()
    # exercise_type = models.CharField()