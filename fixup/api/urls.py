from django.urls import path, include
from .views import UserViewSet, WorkoutHistoryViewSet, SessionsViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list_users', 'post': 'create_user'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve_user', 'put': 'update_user', 'delete': 'destroy_user'}), name='user-detail'),
    path('users/<int:pk>/workout-history/', WorkoutHistoryViewSet.as_view({'get': 'list_sessions', 'post': 'create_session'}), name='user-workout-history'),
]