from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import pyotp

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
    goals = models.CharField(null=True, max_length=500)

    otp_secret = models.CharField(max_length=32, blank=True) 

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()
        self.save()

    def generate_otp_code(self):
        otp = pyotp.TOTP(self.otp_secret, interval=432000, digits=5)
        return otp.now()

    def verify_otp(self, entered_otp_code):
        otp = pyotp.TOTP(self.otp_secret, interval=432000, digits=5)
        expected_otp_code = otp.now()

        return entered_otp_code == expected_otp_code
    
    def __str__(self):
        return self.username
    
class WorkoutHistory(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    session_name = models.CharField(null=True, max_length=100)
    date = models.DateField(default=datetime.date.today)
    session_number = models.PositiveIntegerField(null=True)
    session_duration = models.TimeField(null=True)
    session_notes = models.CharField(null=True, max_length=500)

class Sessions(models.Model):
    workout_history = models.ForeignKey('WorkoutHistory', on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey('ExerciseList', on_delete=models.CASCADE, blank=True, null=True)
    custom_exercise = models.ForeignKey('CustomExerciseList', on_delete=models.CASCADE, blank=True, null=True)
    exercise_number = models.IntegerField(null=True)
    notes = models.CharField(null=True, max_length=500)

# Types of Exercises
class WeightLiftSession(models.Model):
    session = models.ForeignKey('Sessions', on_delete=models.CASCADE, null=True)
    
    WEIGHT_METRIC_OPTIONS = [
        ("kg", "kilograms"),
        ("lb", "pounds")
    ]

    set_number = models.IntegerField(null=True, unique=True)
    warmup_set = models.BooleanField(default=False)
    weight = models.FloatField(null=True)
    kgorlb = models.CharField(null=True, max_length=2, choices=WEIGHT_METRIC_OPTIONS)
    reps = models.IntegerField(null=True)
    inbetween_rest_time = models.TimeField(null=True)

class RunningSession(models.Model):
    session = models.ForeignKey('Sessions', on_delete=models.CASCADE, null=True)
    
    DISTANCE_METRIC_OPTIONS = [
        ("km", "kilometers"),
        ("mi.", "miles")
    ]
        
    pace = models.TimeField(null=True)
    distance = models.FloatField(null=True)
    kmormiles = models.CharField(null=True, max_length=3, choices=DISTANCE_METRIC_OPTIONS)
    time = models.TimeField(null=True)

# Curated Exercise Lists
class ExerciseList(models.Model):
    exercise_name = models.CharField(null=True, max_length=100)
    exercise_type = models.CharField(null=True, max_length=100)

class CustomExerciseList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    custom_exercise_name = models.CharField(null=True, max_length=100)
    custom_exercise_type = models.CharField(null=True, max_length=100)
    linked_exercise = models.ForeignKey(ExerciseList, on_delete=models.SET_NULL, blank=True, null=True)

    #Overrides the custom_exercise_type by replacing it with the linked_exercise exercise_type if linked_exercise is not null
    def save(self, *args, **kwargs):
        if self.linked_exercise:
            linked_exercise_type = self.linked_exercise.exercise_type
            if linked_exercise_type:
                self.custom_exercise_type = linked_exercise_type
        super().save(*args, **kwargs)