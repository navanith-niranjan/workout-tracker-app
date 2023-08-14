from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import WorkoutHistoryViewSet, SessionsViewSet

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/users/<int:user_pk>/workout-history/', views.WorkoutHistoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-workout-history-list'),
    path('api/users/<int:user_pk>/workout-history/<int:pk>/', views.SessionsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-sessions-detail'),
]