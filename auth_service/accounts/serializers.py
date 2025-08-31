from rest_framework import serializers

from auth_service.serializers.base import (
    BaseModelSerializer,
    BaseSerializer,
)
from .models import User


class RegisterSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not self.user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        return data


class PasswordResetRequestSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get("email")
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.user = None

        return data


class PasswordResetSerializer(BaseSerializer):
    token = serializers.CharField(
        write_only=True,
        required=True,
        help_text="The recovery token from the reset link",
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="New password (min 8 characters)",
    )