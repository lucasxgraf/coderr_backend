from rest_framework.permissions import BasePermission


class IsOfferOwner(BasePermission):
    """Allow access only if the requesting user is the owner of the offer."""

    def has_object_permission(self, request, view, obj):
        """Return True if the request user matches the offer's creator."""
        return obj.user == request.user


class IsBusinessUser(BasePermission):
    """Allow access only to users with account type 'business'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a business user."""
        return request.user.type == 'business'
