from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    SEX_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=1, choices=SEX_OPTIONS)
    height = models.CharField(max_length=3)
    weight = models.CharField(max_length=3)

class WorkoutHistory(models.Model):
    pass

class Sessions(models.Model):
    pass

class ExerciseList(models.Model):
    pass