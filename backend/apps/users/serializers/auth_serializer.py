"""
TeamTrack – Auth serializers (register, login).
Validation only; no business logic.
"""
from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.Serializer):
    """Validate registration input."""

    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=128)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    def validate_email(self, value):
        email = (value or "").strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_password(self, value):
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    """Validate login input."""

    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["email"].lower(),
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs
