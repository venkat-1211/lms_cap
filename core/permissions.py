from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        user = request.user

        # ✅ Check authentication first
        if not user or not user.is_authenticated:
            return False

        # ✅ Safe role access
        return getattr(user, "role", None) in self.allowed_roles


class IsAdmin(BaseRolePermission):
    allowed_roles = ["admin"]


class IsManager(BaseRolePermission):
    allowed_roles = ["manager"]


class IsCustomer(BaseRolePermission):
    allowed_roles = ["customer"]