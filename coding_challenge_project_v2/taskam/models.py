from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )


class Project(BaseModel):
    creator = models.ForeignKey(
        User,
        related_name='creator_projects',
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField(
        User,
        related_name='assignees_projects',
        blank=True,
    )


class Task(BaseModel):
    project = models.ForeignKey(
        Project,
        related_name='tasks',
        on_delete=models.CASCADE,
    )
    creator = models.ForeignKey(
        User,
        related_name='creator_tasks',
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField(
        User,
        related_name='assignees_tasks',
        blank=True
    )

