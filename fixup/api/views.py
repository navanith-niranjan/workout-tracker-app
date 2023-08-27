from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import User, WorkoutHistory, Sessions, WeightLiftSession, RunningSession, ExerciseList, CustomExerciseList
from .serializer import UserSerializer, WorkoutHistorySerializer, SessionsSerializer, WeightLiftSessionSerializer, RunningSessionSerializer, ExerciseListSerializer, CustomExerciseListSerializer
from django.db.models import Max
from decouple import config
from rest_framework.permissions import IsAuthenticated
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView

# SOCIAL_GOOGLE_CALLBACK_URL = config('SOCIAL_GOOGLE_CALLBACK_URL')

# class GoogleLogin(SocialLoginView): 
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = SOCIAL_GOOGLE_CALLBACK_URL
#     client_class = OAuth2Client

# class GoogleConnect(SocialConnectView): 
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = SOCIAL_GOOGLE_CALLBACK_URL
#     client_class = OAuth2Client

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    permission_classes = [IsAuthenticated]

    def list_users(self, request): # Fully Functional
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    # def create_user(self, request): # Fully Functional
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated]

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
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
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

    def update_exercise(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        if exercise_entry.exercise:
            previous_exercise_type = exercise_entry.exercise.exercise_type
        if exercise_entry.custom_exercise:
            previous_exercise_type = exercise_entry.custom_exercise.custom_exercise_type

        serializer = self.serializer_class(exercise_entry, data=request.data)
        if serializer.is_valid():
            new_exercise = serializer.validated_data.get("exercise")
            new_custom_exercise = serializer.validated_data.get("custom_exercise")

            if new_exercise and new_custom_exercise:
                return Response({"error": "Both exercise and custom exercise cannot have values"}, status=status.HTTP_400_BAD_REQUEST)

            if new_exercise:
                exercise_entry.custom_exercise = None  # Set custom exercise to null
                exercise_entry.exercise = new_exercise
            elif new_custom_exercise:
                exercise_entry.exercise = None  # Set exercise to null
                exercise_entry.custom_exercise = new_custom_exercise
            
            serializer.save(workout_history=workout_history)

            if new_exercise:
                try:
                    new_exercise = ExerciseList.objects.get(pk=new_exercise.id)
                    new_exercise_type = new_exercise.exercise_type
                except ExerciseList.DoesNotExist:
                    return Response({"error": "New exercise not found"}, status=status.HTTP_404_NOT_FOUND)
            elif new_custom_exercise:
                try:
                    new_custom_exercise = CustomExerciseList.objects.get(pk=new_custom_exercise.id)
                    new_exercise_type = new_custom_exercise.custom_exercise_type
                except CustomExerciseList.DoesNotExist:
                    return Response({"error": "New custom exercise not found"}, status=status.HTTP_404_NOT_FOUND)

            if new_exercise_type != previous_exercise_type:
                if previous_exercise_type == "weightlifting":
                    exercise_entry.weightliftsession_set.all().delete()
                elif previous_exercise_type == "running":
                    exercise_entry.runningsession_set.all().delete()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_exercise(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = self.queryset.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        exercise_entry.delete()
        remaining_exercises = Sessions.objects.filter(workout_history=workout_history, exercise_number__gt=exercise_number)
        for exercise in remaining_exercises:
            exercise.exercise_number -= 1
            exercise.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list_exercise_stats(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if exercise_entry.exercise:
            exercise_type = exercise_entry.exercise.exercise_type
        elif exercise_entry.custom_exercise:
            exercise_type = exercise_entry.custom_exercise.custom_exercise_type
        else:
            exercise_type = None

        if exercise_type == "weightlifting":
            weight_lift_entry = WeightLiftSession.objects.filter(session=exercise_entry)
            if weight_lift_entry.exists():
                serializer = WeightLiftSessionSerializer(weight_lift_entry, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Stats not found"}, status=status.HTTP_404_NOT_FOUND)
        elif exercise_type == "running":
            try:
                running_entry = RunningSession.objects.get(session=exercise_entry)
                serializer = RunningSessionSerializer(running_entry)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RunningSession.DoesNotExist:
                return Response({"error": "Stats not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Exercise type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    def create_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = self.queryset.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if exercise_entry.exercise:
            exercise_type = exercise_entry.exercise.exercise_type
        elif exercise_entry.custom_exercise:
            exercise_type = exercise_entry.custom_exercise.custom_exercise_type
        else:
            exercise_type = None

        if exercise_type == "weightlifting":
            weight_lift_viewset = WeightLiftSessionViewSet(request=request)
            return weight_lift_viewset.create_exercise_stat(request, pk, session_number, exercise_number)
        elif exercise_type == "running":
            running_viewset = RunningSessionViewSet(request=request)
            return running_viewset.create_exercise_stat(request, pk, session_number, exercise_number)
        else:
            return Response({"error": "Exercise type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    def update_exercise_stats(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = self.queryset.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if exercise_entry.exercise:
            exercise_type = exercise_entry.exercise.exercise_type
        elif exercise_entry.custom_exercise:
            exercise_type = exercise_entry.custom_exercise.custom_exercise_type
        else:
            exercise_type = None

        if exercise_type == "weightlifting":
            weight_lift_viewset = WeightLiftSessionViewSet(request=request)
            return weight_lift_viewset.update_exercise_stat(request, pk, session_number, exercise_number)
        elif exercise_type == "running":
            running_viewset = RunningSessionViewSet(request=request)
            return running_viewset.update_exercise_stat(request, pk, session_number, exercise_number)
        else:
            return Response({"error": "Exercise type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy_exercise_stats(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = self.queryset.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if exercise_entry.exercise:
            exercise_type = exercise_entry.exercise.exercise_type
        elif exercise_entry.custom_exercise:
            exercise_type = exercise_entry.custom_exercise.custom_exercise_type
        else:
            exercise_type = None

        if exercise_type == "weightlifting":
            weight_lift_viewset = WeightLiftSessionViewSet(request=request)
            return weight_lift_viewset.destroy_exercise_stat(request, pk, session_number, exercise_number)
        elif exercise_type == "running":
            running_viewset = RunningSessionViewSet(request=request)
            return running_viewset.destroy_exercise_stat(request, pk, session_number, exercise_number)
        else:
            return Response({"error": "Exercise type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

class WeightLiftSessionViewSet(viewsets.ModelViewSet):
    queryset = WeightLiftSession.objects.all()
    serializer_class = WeightLiftSessionSerializer

    permission_classes = [IsAuthenticated]

    def create_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            max_set_number = WeightLiftSession.objects.filter(session=exercise_entry).aggregate(Max('set_number'))['set_number__max']
            set_number = (max_set_number or 0) + 1
            serializer.save(session=exercise_entry, set_number=set_number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        set_number = request.data.get('set_number')  # Get the set_number from the request data

        try:
            weight_lift_entry = WeightLiftSession.objects.get(session=exercise_entry, set_number=set_number)
        except WeightLiftSession.DoesNotExist:
            return Response({"error": "Set not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(weight_lift_entry, data=request.data)
        if serializer.is_valid():
            serializer.save(session=exercise_entry, set_number=set_number)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        set_number = request.data.get('set_number')  # Get the set_number from the request data

        if set_number is not None:
            try:
                weight_lift_entry = WeightLiftSession.objects.filter(session=exercise_entry, set_number=set_number)
                weight_lift_entry.delete()

                # Correct the ordering of sets
                remaining_sets = WeightLiftSession.objects.filter(session=exercise_entry, set_number__gt=set_number)
                for remaining_set in remaining_sets:
                    remaining_set.set_number -= 1
                    remaining_set.save()
            except WeightLiftSession.DoesNotExist:
                return Response({"error": "Stats not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            exercise_entry.weightliftsession_set.all().delete()  

        return Response(status=status.HTTP_204_NO_CONTENT)

class RunningSessionViewSet(viewsets.ModelViewSet):
    queryset = RunningSession.objects.all()
    serializer_class = RunningSessionSerializer

    permission_classes = [IsAuthenticated]

    def create_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        if RunningSession.objects.filter(session=exercise_entry).exists():
            return Response({"error": "Running stats entry already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(session=exercise_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
            running_entry = RunningSession.objects.get(session=exercise_entry)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(running_entry, data=request.data)
        if serializer.is_valid():
            serializer.save(session=exercise_entry)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_exercise_stat(self, request, pk=None, session_number=None, exercise_number=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history = WorkoutHistory.objects.get(user=user, session_number=session_number)
            exercise_entry = Sessions.objects.get(workout_history=workout_history, exercise_number=exercise_number)
            running_entry = RunningSession.objects.get(session=exercise_entry)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Sessions.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        running_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ExerciseListViewSet(viewsets.ModelViewSet):
    queryset = ExerciseList.objects.all()
    serializer_class = ExerciseListSerializer

    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated]

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

