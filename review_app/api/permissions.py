from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Allow access only to authenticated users with account type 'customer'."""

    def has_permission(self, request, view):
        """Return True if the user is authenticated and is a customer."""
        return request.user.is_authenticated and request.user.type == 'customer'


class IsReviewerAuthor(BasePermission):
    """Allow access only if the requesting user is the author of the review."""

    def has_object_permission(self, request, view, obj):
        """Return True if the request user matches the review's reviewer."""
        return request.user == obj.reviewer
