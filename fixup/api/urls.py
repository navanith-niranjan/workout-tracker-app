from django.urls import path, include
from .views import UserViewSet, WorkoutHistoryViewSet, SessionsViewSet, ExerciseListViewSet, CustomExerciseListViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list_users', 'post': 'create_user'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve_user', 'put': 'update_user', 'delete': 'destroy_user'}), name='user-detail'),
    path('users/<int:pk>/workout-history/', WorkoutHistoryViewSet.as_view({'get': 'list_sessions', 'post': 'create_session'}), name='user-workout-history'),
    path('users/<int:pk>/workout-history/<int:session_number>/', WorkoutHistoryViewSet.as_view({'get': 'retrieve_session', 'put': 'update_session', 'delete': 'destroy_session'}), name='user-workout-history-session'),
    path('users/<int:pk>/workout-history/<int:session_number>/details/', SessionsViewSet.as_view({'get': 'list_exercises', 'post': 'create_exercise'}), name = 'session-details'),
    path('users/<int:pk>/workout-history/<int:session_number>/details/<int:exercise_number>/', SessionsViewSet.as_view({'get': 'retrieve_exercise', 'put': 'update_exercise', 'delete': 'destroy_exercise'}), name = 'exercise-details'),
    path('users/<int:pk>/workout-history/<int:session_number>/details/<int:exercise_number>/stats/', SessionsViewSet.as_view({'get': 'list_exercise_stats', 'post':'create_exercise_stat', 'put': 'update_exercise_stats', 'delete': 'destroy_exercise_stats'}), name = 'exercise-stats'),

    path('exercise-list/', ExerciseListViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'exercise-list'),
    path('users/<int:pk>/custom-exercise-list/', CustomExerciseListViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'custom-exercise-list'),
    path('users/<int:pk>/custom-exercise-list/<int:custom_exercise_pk>/', CustomExerciseListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name = 'custom-exercise-detail')
]