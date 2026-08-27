from typing import Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import AuthUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as TOPSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as TRSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from lms.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "avatar",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "phone", "city", "avatar", "payments")


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for User instance creation
    """

    class Meta:
        model = User
        fields = ("email", "username", "password")


class TokenObtainPairSerializer(TOPSerializer):

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        token["user"] = user

        return token


class TokenRefreshSerializer(TRSerializer):

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh_token_str = attrs["refresh"]
        refresh_token = RefreshToken(refresh_token_str)

        user_id = refresh_token.payload.get("user_id")
        if user_id:
            user = User.objects.get(id=user_id)
            data["username"] = user.username
            data["email"] = user.email

        return data
