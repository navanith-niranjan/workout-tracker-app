from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import User
from .models import WorkoutHistory
from .models import Sessions
from .models import WeightLiftSession
from .models import RunningSession
from .models import ExerciseList
from .serializer import UserSerializer
from .serializer import WorkoutHistorySerializer
from .serializer import SessionsSerializer
from .serializer import WeightLiftSessionSerializer
from .serializer import RunningSessionSerializer
from .serializer import ExerciseListSerializer
from django.db.models import Max

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def list_users(self, request): # Fully Functional
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create_user(self, request): # Fully Functional
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_user(self, request, pk=None): # Fully Functional
        try:
            user = self.queryset.get(pk=pk)
            serializer = self.serializer_class(user)
            #-------------------- I added this to users retrieve in order to view user workout histories
            workout_history = WorkoutHistory.objects.filter(user=user)
            workout_history_serializer = WorkoutHistorySerializer(workout_history, many=True)
            user_data = serializer.data
            user_data['workout_history'] = workout_history_serializer.data
            return Response(user_data)
            #------------------- delete this if you dont want to see that
            # return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404

    def update_user(self, request, pk=None): # Fully Functional
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_user(self, request, pk=None): # Fully Functional
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WorkoutHistoryViewSet(viewsets.ModelViewSet):
    queryset = WorkoutHistory.objects.all()
    serializer_class = WorkoutHistorySerializer

    def list_sessions(self, request, pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        workout_history_entries = self.queryset.filter(user=pk)
        serializer = self.serializer_class(workout_history_entries, many=True)
        return Response(serializer.data)

    def create_session(self, request, pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            max_id = WorkoutHistory.objects.filter(user=user).aggregate(Max('session_number'))['session_number__max']
            session_number = (max_id or 0) + 1
            serializer.save(user=user, session_number=session_number) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_session(self, request, pk=None, session_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, session_number=session_number)
            serializer = self.serializer_class(workout_history_entry)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    def update_session(self, request, pk=None, session_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, session_number=session_number)
        except User.DoesNotExist:
            raise Http404
        except WorkoutHistory.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(workout_history_entry, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, session_number=session_number)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_session(self, request, pk=None, session_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, session_number=session_number)
        except User.DoesNotExist:
            raise Http404
        except WorkoutHistory.DoesNotExist:
            raise Http404

        workout_history_entry.delete()

        remaining_records = WorkoutHistory.objects.filter(user=user, session_number__gt=session_number)
        for record in remaining_records:
            record.session_number -= 1
            record.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer

    def list_exercises(self, request, pk=None, session_number=None): #Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Workout History not found"}, status=status.HTTP_404_NOT_FOUND)

        jsonResponse = []

        for session in workout_history.sessions_set.all():
            if session.exercise:    
                exercise_data = {
                    "id": session.id,
                    "exercise_number": session.exercise_number,
                    "workout_history_id": session.workout_history.id,
                    "session_number": session_number,
                    "exercise_name": session.exercise.exercise_name,
                    "exercise_type": session.exercise.exercise_type,
                    "notes": session.notes
                }
            if session.custom_exercise:
                exercise_data = {
                    "id": session.id,
                    "exercise_number": session.exercise_number,
                    "workout_history_id": session.workout_history.id,
                    "session_number": session_number,
                    "exercise_name": session.custom_exercise.custom_exercise_name,
                    "exercise_type": session.custom_exercise.custom_exercise_type,
                    "notes": session.notes
                }
            jsonResponse.append(exercise_data)    

        if jsonResponse:
            return Response(jsonResponse, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Details not found"}, status=status.HTTP_404_NOT_FOUND)

    def create_exercise(self, request, pk=None, session_number=None):
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            max_exercise_number = Sessions.objects.filter(workout_history=workout_history).aggregate(Max('exercise_number'))['exercise_number__max']
            exercise_number = (max_exercise_number or 0) + 1
            serializer.save(workout_history=workout_history, exercise_number=exercise_number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def create_exercise_info(self, request, pk=None, session_number=None, exercise_number=None):
    #     # Determine the exercise type based on the exercise_number
    #     exercise = ExerciseList.objects.get(exercise_number=exercise_number)
    #     exercise_id = exercise.id
    #     try:
    #         exercise = ExerciseList.objects.get(id=exercise_id)
    #     except ExerciseList.DoesNotExist:
    #         return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     exercise_type = exercise.exercise_type

    #     if exercise_type == "weightlifting":
    #         return WeightLiftSessionViewSet.as_view({'post': 'create_set'})(request)
    #     elif exercise_type == "running":
    #         return RunningSessionViewSet.as_view({'post': 'create_info'})(request)
    #     else:
    #         return Response({"error": "Invalid exercise type"}, status=status.HTTP_400_BAD_REQUEST)

class WeightLiftSessionViewSet(viewsets.ModelViewSet):
    queryset = WeightLiftSession.objects.all()
    serializer_class = WeightLiftSessionSerializer

    def create_set(self, request):
        return Response({"wow"})

class RunningSessionViewSet(viewsets.ModelViewSet):
    queryset = RunningSession.objects.all()
    serializer_class = RunningSessionSerializer
    
class ExerciseListViewSet(viewsets.ModelViewSet):
    def list(self, request):
        exercises = ExerciseList.objects.all()
        serializer = ExerciseListSerializer(exercises, many=True)
        return Response(serializer.data)
    
    def create(self, request, format=None):
        serializer = ExerciseListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

