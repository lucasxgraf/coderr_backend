from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow access only to users with account type 'customer'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a customer."""
        return request.user.type == 'customer'


class IsBusinessUser(BasePermission):
    """Allow access only to users with account type 'business'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a business user."""
        return request.user.type == 'business'


class IsAdminUser(BasePermission):
    """Allow access only to staff/admin users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user has staff privileges."""
        return request.user.is_staff
