from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdmin(BasePermission):
    """Доступ только администраторам."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        )


class IsModerator(BasePermission):
    """Доступ только модераторам."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )


class IsAdminOrModerator(BasePermission):
    """Доступ администраторам и модераторам."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role in ('admin', 'moderator')
                or request.user.is_superuser
            )
        )
