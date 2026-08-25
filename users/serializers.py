from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "phone", "city", "avatar")


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model
    """

    class Meta:
        model = Payment
        fields = "__all__"
