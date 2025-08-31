from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.cache import cache
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from .serializers import (
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
)

RECOVERY_KEY = "recovery::"
RECOVERY_KEY_EXP = 60 * 10


@swagger_auto_schema(
    operation_summary="Register a new user",
    operation_description="This endpoint allows new users to register with email, username, and password.",
    responses={201: openapi.Response("Registration successful")},
    security=[],
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(
            {
                "status": True,
                "msg": "Registration successful",
                "data": serializer.data,
            },
            status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    message = "Login successful"

    @swagger_auto_schema(
        operation_description="Login with email and password.",
        request_body=LoginSerializer,
        responses={200: openapi.Response("Login successful")},
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.user

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
            }
        )


class RequestTokenView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    message = "Password reset initialized"

    @swagger_auto_schema(
        operation_description="Request a password reset token using email address.",
        request_body=PasswordResetRequestSerializer,
        responses={200: openapi.Response("Password reset initialized")},
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        token = None
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            key = f"{RECOVERY_KEY}{token}"
            cache.set(key, user.email, RECOVERY_KEY_EXP)

        return Response({"token": token}, status.HTTP_200_OK)


class ResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = []
    message = "Password reset successful"

    @swagger_auto_schema(
        operation_description="Reset password with token and new password.",
        request_body=PasswordResetSerializer,
        responses={200: openapi.Response("Password reset successful")},
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        key = f"{RECOVERY_KEY}{token}"
        email = cache.get(key)

        if not email:
            raise serializers.ValidationError("Invalid or expired token.")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found.")

        user.set_password(password)
        user.save()

        cache.delete(key)
        return Response(status.HTTP_200_OK)
