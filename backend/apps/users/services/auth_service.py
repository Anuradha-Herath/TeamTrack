"""
TeamTrack – Auth service.
Business logic for registration and authentication; no token issuance (handled in views with simplejwt).
"""
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from core.exceptions import AuthenticationError

User = get_user_model()


class AuthService:
    """Authentication business logic."""

    @staticmethod
    def register_user(validated_data):
        """
        Create a new user with the given validated data.
        Password is hashed by Django when set via set_password.
        Returns the created User.
        """
        email = validated_data["email"].lower()
        password = validated_data["password"]
        first_name = validated_data.get("first_name", "").strip()
        last_name = validated_data.get("last_name", "").strip()

        user = User(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name,
            role=User.Role.TEAM_MEMBER,
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def authenticate_user(email, password, request=None):
        """
        Authenticate user by email and password.
        Returns User if valid; raises AuthenticationError if invalid.
        """
        user = authenticate(
            request=request,
            username=email.lower(),
            password=password,
        )
        if not user:
            raise AuthenticationError(message="Invalid email or password.")
        return user
