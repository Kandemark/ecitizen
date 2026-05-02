from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to object owners and staff users."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Write access restricted to staff; read allowed for all."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class CanManageCounty(permissions.BasePermission):
    """Only users assigned to a county can manage its data."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'county') and hasattr(request.user, 'profile'):
            return obj.county == request.user.profile.county
        return False
