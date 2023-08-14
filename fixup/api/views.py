from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import User
from .serializer import UserSerializer
from .models import WorkoutHistory
from .serializer import WorkoutHistorySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def list(self, request):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WorkoutHistoryViewSet(viewsets.ModelViewSet):
    queryset = WorkoutHistory.objects.all()
    serializer_class = WorkoutHistorySerializer

    def list(self, request):
        workout_history_entries = self.queryset.all()
        serializer = self.serializer_class(workout_history_entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            workout_history = self.queryset.get(pk=pk)
            serializer = self.serializer_class(workout_history)
            return Response(serializer.data)
        except WorkoutHistory.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        try:
            workout_history = self.queryset.get(pk=pk)
        except WorkoutHistory.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(workout_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            workout_history = self.queryset.get(pk=pk)
        except WorkoutHistory.DoesNotExist:
            raise Http404

        workout_history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)