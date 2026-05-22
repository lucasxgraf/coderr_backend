from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'customer'
    
class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'business'
    
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff