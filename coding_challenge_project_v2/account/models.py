from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    DEVELOPER = 'developer'
    PRODUCT_MANAGER = 'product_manager'
    ROLES = (
        (DEVELOPER, 'Developer'),
        (PRODUCT_MANAGER, 'Product Manager')
    )

    role = models.CharField(
        choices=ROLES,
        max_length=30,
        blank=True,
        null=True,
    )


