from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'
    
class IsReviewerAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
