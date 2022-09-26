from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .permissions import ProjectViewPermission, TaskViewPermission
from .models import Project, Task
from .serializers import (
    ProjectSerializer,
    CreateProjectSerializer,
    AssignProjectTaskSerializer,
    TaskSerializer,
    CreateTaskSerializer,
)


@permission_classes((IsAuthenticated, ProjectViewPermission, ))
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


@permission_classes((IsAuthenticated, TaskViewPermission, ))
class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
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
        'project_id',
    )
    filterset_fields = (
        'creator__username',
        'assignees__username',
        'project_id',
    )

    def create(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            TaskSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk):
        task = get_object_or_404(
            Task,
            id=pk
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
