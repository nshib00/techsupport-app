from rest_framework.permissions import BasePermission


class IsSupportUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'support'