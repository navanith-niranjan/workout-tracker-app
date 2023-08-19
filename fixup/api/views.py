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
from .models import CustomExerciseList
from .serializer import UserSerializer
from .serializer import WorkoutHistorySerializer
from .serializer import SessionsSerializer
from .serializer import WeightLiftSessionSerializer
from .serializer import RunningSessionSerializer
from .serializer import ExerciseListSerializer
from .serializer import CustomExerciseListSerializer
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

        workout_history_entries = self.queryset.filter(user=user)
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
            workout_history_entry = self.queryset.get(user=user, session_number=session_number)
            serializer = self.serializer_class(workout_history_entry)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    def update_session(self, request, pk=None, session_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=user, session_number=session_number)
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
            workout_history_entry = self.queryset.get(user=user, session_number=session_number)
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

    def list_exercises(self, request, pk=None, session_number=None): # Fully Functional
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

    def create_exercise(self, request, pk=None, session_number=None): # Fully Functional
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
    
    def retrieve_exercise(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = self.queryset.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if exercise_entry.exercise:
            exercise_data = {
                "id": exercise_entry.id,
                "exercise_number": exercise_entry.exercise_number,
                "workout_history_id": exercise_entry.workout_history.id,
                "session_number": session_number,
                "exercise_name": exercise_entry.exercise.exercise_name,
                "exercise_type": exercise_entry.exercise.exercise_type,
                "notes": exercise_entry.notes
            }
        if exercise_entry.custom_exercise:
            exercise_data = {
                "id": exercise_entry.id,
                "exercise_number": exercise_entry.exercise_number,
                "workout_history_id": exercise_entry.workout_history.id,
                "session_number": session_number,
                "exercise_name": exercise_entry.custom_exercise.custom_exercise_name,
                "exercise_type": exercise_entry.custom_exercise.custom_exercise_type,
                "notes": exercise_entry.notes
            }

        return Response(exercise_data, status=status.HTTP_200_OK)

    def update_exercise():
        pass

    def destroy_exercise():
        pass

    def list_exercise_stats():
        pass

    def create_exercise_stat():
        pass

    def update_exercise_stats():
        pass

    def destroy_exercise_stats():
        pass

    def update_specific_stat():
        pass

    def destroy_specific_stat():
        pass

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

class RunningSessionViewSet(viewsets.ModelViewSet):
    queryset = RunningSession.objects.all()
    serializer_class = RunningSessionSerializer
    
class ExerciseListViewSet(viewsets.ModelViewSet):
    queryset = ExerciseList.objects.all()
    serializer_class = ExerciseListSerializer

    def list(self, request): # Fully Functional
        exercises = self.queryset.all()
        serializer = self.serializer_class(exercises, many=True)
        return Response(serializer.data)
    
    def create(self, request): # Fully Functional
        serializer = ExerciseListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Not neccessary for users, may be needed for admin
    
    # def retrieve(self, request, pk=None):
    #     try:
    #         exercise = self.queryset.get(pk=pk)
    #         serializer = self.serializer_class(exercise)
    #         return Response(serializer.data)
    #     except ExerciseList.DoesNotExist:
    #         raise Http404
    
    # def update(self, request, pk=None):
    #     try:
    #         exercise = self.queryset.get(pk=pk)
    #     except ExerciseList.DoesNotExist:
    #         raise Http404

    #     serializer = self.serializer_class(exercise, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def destroy(self, request, pk=None):
    #     try:
    #         exercise = self.queryset.get(pk=pk)
    #     except ExerciseList.DoesNotExist:
    #         raise Http404

    #     exercise.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CustomExerciseListViewSet(viewsets.ModelViewSet): 
    queryset = CustomExerciseList.objects.all()
    serializer_class = CustomExerciseListSerializer

    def list(self, request, pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        custom_exercises = self.queryset.filter(user=user)
        serializer = self.serializer_class(custom_exercises, many=True)
        return Response(serializer.data)
    
    def create(self, request, pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomExerciseListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None, custom_exercise_pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            custom_exercise = self.queryset.get(user=user, pk=custom_exercise_pk)
            serializer = self.serializer_class(custom_exercise)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomExerciseList.DoesNotExist:
            raise Http404
    
    def update(self, request, pk=None, custom_exercise_pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            custom_exercise = self.queryset.get(user=user, pk=custom_exercise_pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomExerciseList.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(custom_exercise, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, custom_exercise_pk=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            custom_exercise = self.queryset.get(user=user, pk=custom_exercise_pk)
        except CustomExerciseList.DoesNotExist:
            raise Http404

        custom_exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

