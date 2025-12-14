from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

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


class IsAdminOrReadOnly(IsAdmin):
    """Разрешает чтение всем, запись только админам."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


# ДОБАВЬТЕ ЭТОТ НОВЫЙ PERMISSION:
class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Разрешает чтение всем.
    Разрешает запись только автору, модератору или админу.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if hasattr(obj, 'author') and obj.author == user:
            return True

        if hasattr(user, 'role'):
            if user.role in ['moderator', 'admin']:
                return True

        if user.is_superuser:
            return True

        return False
