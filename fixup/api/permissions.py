from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow owners to read, create, and modify their own objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Read permissions (GET, HEAD, OPTIONS)
            return True

        # Write permissions (POST, PUT, PATCH, DELETE) allowed only for object's owner
        if request.method == 'POST' or obj.owner == request.user:
            return True
        
        return False