from rest_framework.permissions import BasePermission


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'business'
