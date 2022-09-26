from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Project, Task
from account.serializers import UserSerializer
from .exceptions import(
    AssigneesUsernamesTypeException,
    NotExistingDeveloperException,
    NotFoundProjectException,
)

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    assignees = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
        )

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        project = Project.objects.create(**validated_data)
        return project


class AssignProjectTaskSerializer(serializers.Serializer):
    assignees_usernames = serializers.JSONField()

    def validate_assignees_usernames(self, assignees_usernames):
        if not isinstance(assignees_usernames, (list, tuple)):
            raise serializers.ValidationError(AssigneesUsernamesTypeException())
        self.developers = User.objects.filter(
            role='developer'
        )
        developers_username = self.developers.values_list(
            'username',
            flat=True
        )
        incorrect_usernames = [
            username for username in assignees_usernames if username not in developers_username
        ]
        if len(incorrect_usernames) > 0:
            raise serializers.ValidationError(NotExistingDeveloperException(incorrect_usernames))
        return assignees_usernames

    def update(self, instance, validated_data):
        assignees = self.developers.filter(username__in=validated_data.get('assignees_usernames'))
        self.instance.assignees.set(assignees)
        return self.instance


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    assignees = UserSerializer(many=True)

    class Meta:
        model = Task
        exclude = ('project',)


class CreateTaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'project_id'
        )

    def validate_project_id(self, project_id):
        project = Project.objects.filter(id=project_id)
        if project:
            return project_id
        raise serializers.ValidationError(NotFoundProjectException())

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        task = Task.objects.create(**validated_data)
        return task

