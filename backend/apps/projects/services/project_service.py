"""
TeamTrack – Project service.
Business logic for project CRUD and member management.
Permission checks (admin or project owner/admin) are done in the permission class; service assumes caller is allowed where applicable.
"""
from django.db.models import QuerySet

from core.exceptions import NotFoundError, PermissionDeniedError, ConflictError

from apps.users.models import User
from apps.projects.models import Project, ProjectMember


class ProjectService:
    """Project and membership business logic."""

    @staticmethod
    def list_projects_for_user(user: User) -> QuerySet:
        """
        Return projects the user can see: all if admin, else only projects they are a member of.
        Ordered by -updated_at.
        """
        if getattr(user, "role", None) == User.Role.ADMIN:
            return Project.objects.all().select_related("created_by").order_by("-updated_at")
        return (
            Project.objects.filter(members__user=user)
            .select_related("created_by")
            .distinct()
            .order_by("-updated_at")
        )

    @staticmethod
    def get_project_by_id(project_id: int, user: User) -> Project:
        """
        Return project by id. Admin can access any; others only if member.
        Raises NotFoundError if not found or no access (no leak of existence).
        """
        try:
            project = Project.objects.select_related("created_by").get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFoundError(message="Project not found.")

        if getattr(user, "role", None) == User.Role.ADMIN:
            return project
        if project.created_by_id == user.pk:
            return project
        if ProjectMember.objects.filter(project=project, user=user).exists():
            return project
        raise NotFoundError(message="Project not found.")

    @staticmethod
    def create_project(user: User, validated_data: dict) -> Project:
        """Create project and add creator as PROJECT_ADMIN member. Returns created project."""
        project = Project.objects.create(
            name=validated_data["name"],
            description=validated_data.get("description", ""),
            status=validated_data.get("status", Project.Status.ACTIVE),
            created_by=user,
        )
        ProjectMember.objects.create(
            project=project,
            user=user,
            role=ProjectMember.Role.PROJECT_ADMIN,
        )
        return project

    @staticmethod
    def update_project(project_id: int, validated_data: dict) -> Project:
        """Update project fields. Caller must have been checked for modify permission."""
        project = Project.objects.get(pk=project_id)
        for key in ("name", "description", "status"):
            if key in validated_data:
                setattr(project, key, validated_data[key])
        project.save(update_fields=[k for k in ("name", "description", "status") if k in validated_data])
        return project

    @staticmethod
    def delete_project(project_id: int) -> None:
        """Delete project (cascade deletes members). Caller must have been checked for modify permission."""
        Project.objects.filter(pk=project_id).delete()

    @staticmethod
    def can_modify_project(user: User, project: Project) -> bool:
        """True if user is global admin, project creator, or project member with PROJECT_ADMIN role."""
        if getattr(user, "role", None) == User.Role.ADMIN:
            return True
        if project.created_by_id == user.pk:
            return True
        return ProjectMember.objects.filter(
            project=project,
            user=user,
            role=ProjectMember.Role.PROJECT_ADMIN,
        ).exists()

    @staticmethod
    def list_members(project: Project) -> QuerySet:
        """Return project members (ProjectMember with user)."""
        return project.members.select_related("user").all()

    @staticmethod
    def add_member(project: Project, user_id: int, role: str, added_by: User) -> ProjectMember:
        """
        Add user as project member. Raises ConflictError if already a member.
        Caller must have been checked for modify permission.
        """
        if ProjectMember.objects.filter(project=project, user_id=user_id).exists():
            raise ConflictError(message="User is already a member of this project.")
        target_user = User.objects.filter(pk=user_id).first()
        if not target_user:
            raise NotFoundError(message="User not found.")
        return ProjectMember.objects.create(project=project, user=target_user, role=role)

    @staticmethod
    def remove_member(project: Project, user_id: int, removed_by: User) -> None:
        """
        Remove user from project. Caller must have been checked for modify permission.
        Raises NotFoundError if not a member.
        """
        membership = ProjectMember.objects.filter(project=project, user_id=user_id).first()
        if not membership:
            raise NotFoundError(message="User is not a member of this project.")
        membership.delete()
