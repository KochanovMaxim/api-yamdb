from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return bool(user and getattr(user, 'is_admin', False))


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or getattr(request, 'user', None)
            and getattr(request.user, 'is_admin', False)
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        return bool(
            request.method in SAFE_METHODS
            or (user and user.is_authenticated and (
                obj.author == user
                or getattr(user, 'is_admin', False)
                or getattr(user, 'is_moderator', False)
            ))
        )
