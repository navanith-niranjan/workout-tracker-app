from rest_framework import serializers
from .models import User, WorkoutHistory, Sessions, ExerciseList, CustomExerciseList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WorkoutHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutHistory
        fields = '__all__'

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'

class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseList
        fields = '__all__'

class CustomExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomExerciseList
        fields = '__all__'