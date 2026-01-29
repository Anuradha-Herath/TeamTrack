"""
TeamTrack – Project and ProjectMember models.
"""
from django.conf import settings
from django.db import models


class Project(models.Model):
    """Project container; created_by is the owner."""

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        ARCHIVED = "ARCHIVED", "Archived"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """Many-to-many between User and Project with role. Unique (user, project)."""

    class Role(models.TextChoices):
        PROJECT_ADMIN = "PROJECT_ADMIN", "Project Admin"
        MEMBER = "MEMBER", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "project"], name="unique_project_member"),
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["project"]),
        ]

    def __str__(self):
        return f"{self.user.email} in {self.project.name} ({self.role})"
