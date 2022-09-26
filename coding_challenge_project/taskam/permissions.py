from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectViewPermission(BasePermission):
    def has_permission(self, request, view):
        user_role = request.user.role
        if request.method in ['POST', 'PATCH']:
            return user_role == User.PRODUCT_MANAGER
        else:
            return user_role == User.DEVELOPER or user_role == User.PRODUCT_MANAGER


class TaskViewPermission(BasePermission):
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == User.DEVELOPER or user_role == User.PRODUCT_MANAGER
