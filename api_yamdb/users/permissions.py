from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdmin(BasePermission):
    """Доступ только администраторам (включая superuser)."""
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return bool(
            user.is_superuser or getattr(user, 'role', None) == User.ADMIN
        )


class IsModerator(BasePermission):
    """Доступ только модераторам."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )
