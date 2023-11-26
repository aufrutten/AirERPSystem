
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAnonymousOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)
