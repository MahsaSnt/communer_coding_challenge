from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .permissions import ProjectPermission, TaskPermission
from .models import Project, Task
from .serializers import (
    ProjectSerializer,
    CreateProjectSerializer,
    AssignProjectTaskSerializer,
    TaskSerializer,
    CreateTaskSerializer,
)


@permission_classes((IsAuthenticated, ProjectPermission, ))
class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = (
        'get',
        'post',
        'patch',
    )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title',
        'created_at'
    )
    filterset_fields = (
        'creator__username',
        'assignees__username',
    )

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(creator=user) | Q(assignees=user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = CreateProjectSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            ProjectSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk):
        project = get_object_or_404(
            Project,
            id=pk
        )
        serializer = AssignProjectTaskSerializer(
            instance=project,
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            ProjectSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )


@permission_classes((IsAuthenticated, TaskPermission, ))
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    http_method_names = (
        'get',
        'post',
        'patch',
    )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title',
        'created_at',
    )
    filterset_fields = (
        'assignees__username',
    )

    def get_queryset(self):
        user = self.request.user
        project_id = self.request.parser_context['kwargs'].get('project_id')
        return Task.objects.filter(
            Q(project_id=project_id) & (Q(project__creator=user) | Q(project__assignees=user))
        ).distinct()

    def create(self, request, project_id, *args, **kwargs):
        serializer = CreateTaskSerializer(
            data=request.data,
            context={
                'request': request,
                'project_id': project_id
            }
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            TaskSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk, project_id, *args, **kwargs):
        task = get_object_or_404(
            Task,
            id=pk,
            project_id=project_id,
        )
        serializer = AssignProjectTaskSerializer(
            instance=task,
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            TaskSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )
