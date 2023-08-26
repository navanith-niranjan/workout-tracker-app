from rest_framework import permissions

class IsSelf(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own User object.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user