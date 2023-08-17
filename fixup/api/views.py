from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import User
from .models import WorkoutHistory
from .models import Sessions
from .serializer import UserSerializer
from .serializer import WorkoutHistorySerializer
from .serializer import SessionsSerializer
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
            max_id = WorkoutHistory.objects.filter(user=user).aggregate(Max('user_specific_id'))['user_specific_id__max']
            user_specific_id = (max_id or 0) + 1
            serializer.save(user=user, user_specific_id=user_specific_id) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_session(self, request, pk=None, session_id=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, user_specific_id=session_id)
            serializer = self.serializer_class(workout_history_entry)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except WorkoutHistory.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    def update_session(self, request, pk=None, session_id=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, user_specific_id=session_id)
        except User.DoesNotExist:
            raise Http404
        except WorkoutHistory.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(workout_history_entry, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, user_specific_id=session_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_session(self, request, pk=None, session_id=None): # Fully Functional
        try:
            user = User.objects.get(pk=pk)
            workout_history_entry = self.queryset.get(user=pk, user_specific_id=session_id)
        except User.DoesNotExist:
            raise Http404
        except WorkoutHistory.DoesNotExist:
            raise Http404

        workout_history_entry.delete()

        remaining_records = WorkoutHistory.objects.filter(user=user, user_specific_id__gt=session_id)
        for record in remaining_records:
            record.user_specific_id -= 1
            record.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer

    def list(self, request):
        sessions_entries = self.queryset.all()
        serializer = self.serializer_class(sessions_entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            session = self.queryset.get(pk=pk)
            serializer = self.serializer_class(session)
            return Response(serializer.data)
        except Sessions.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        try:
            session = self.queryset.get(pk=pk)
        except Sessions.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            session = self.queryset.get(pk=pk)
        except Sessions.DoesNotExist:
            raise Http404

        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

