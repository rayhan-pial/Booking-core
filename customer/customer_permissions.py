from rest_framework.permissions import BasePermission
from coreapp.roles import UserRoles


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.CUSTOMER)
