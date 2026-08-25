from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model
    """
    title = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("user", "title", "date", "amount", "course", "lesson", "method",)

    def get_title(self, obj):
        if obj.course:
            return obj.course.title
        elif obj.lesson:
            return obj.lesson.title


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "phone", "city", "avatar", "payments")
