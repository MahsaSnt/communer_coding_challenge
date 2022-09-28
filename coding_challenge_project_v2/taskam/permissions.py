from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Project
User = get_user_model()


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_role = user.role
        if request.method == 'POST':
            return user_role == User.PRODUCT_MANAGER
        elif request.method == 'PATCH':
            pk = request.parser_context['kwargs'].get('pk')
            project = get_object_or_404(
                Project,
                id=pk
            )
            return project.creator == user
        else:
            return user_role == User.DEVELOPER or user_role == User.PRODUCT_MANAGER


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        project_id = request.parser_context['kwargs'].get('project_id')
        project = get_object_or_404(
            Project,
            id=project_id
        )
        user = request.user
        return project.creator == user or user in project.assignees.all()
