from rest_framework.permissions import BasePermission
from users.models import User



class IsSupportUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
            return request.user.role == 'support' and request.user.is_active
        return False
    

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
            return request.user.role == 'admin' and request.user.is_active
        return False
    