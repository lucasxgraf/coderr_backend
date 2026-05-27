from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allow access only if the requesting user is the profile owner."""

    def has_object_permission(self, request, view, obj):
        """Return True if the request user matches the profile object directly."""
        return obj == request.user
