"""
TeamTrack – User model.
Extends AbstractUser with role (ADMIN / TEAM_MEMBER) and email as primary identifier.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user with email as USERNAME_FIELD and role for global permissions.
    """
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEAM_MEMBER = "TEAM_MEMBER", "Team Member"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TEAM_MEMBER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
