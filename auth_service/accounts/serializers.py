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
