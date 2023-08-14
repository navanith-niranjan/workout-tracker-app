from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import WorkoutHistoryViewSet, SessionsViewSet

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'workout-history', WorkoutHistoryViewSet)
router.register(r'sessions', SessionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]