from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    SEX_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
        ("N", "Not Specified")
    ]

    age = models.IntegerField(null=True)
    sex = models.CharField(null=True, max_length=1, choices=SEX_OPTIONS)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

class WorkoutHistory(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    session_name = models.CharField(null=True, max_length=100)
    date = models.DateField(null=True)

class Sessions(models.Model):
    workout_history = models.ForeignKey('WorkoutHistory', on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey('ExerciseList', on_delete=models.CASCADE, null=True)
    sets = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    kgorlb = models.CharField(null=True, max_length=3)  # Assuming it's either "kg" or "lb"
    reps = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pace = models.TimeField(null=True)
    distance = models.FloatField(null=True)
    kmormiles = models.CharField(null=True, max_length=6)  # Assuming it's either "kilometers" or "miles"
    notes = models.CharField(null=True, max_length=500)
    session_duration = models.TimeField(null=True)

class ExerciseList(models.Model):
    exercise_name = models.CharField(null=True, max_length=100)
    exercise_type = models.CharField(null=True, max_length=100)