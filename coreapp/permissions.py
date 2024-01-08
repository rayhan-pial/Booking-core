from rest_framework.permissions import BasePermission
from .roles import UserRoles


class IsVendorUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == UserRoles.VENDOR)


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == UserRoles.CUSTOMER)

