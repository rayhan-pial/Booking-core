from rest_framework.permissions import BasePermission
from coreapp.roles import UserRoles
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class VendorPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.VENDOR)
