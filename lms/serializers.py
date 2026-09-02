from rest_framework import serializers

from lms.models import Course, CourseSubscription, Lesson, Payment
from lms.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model
    """

    video_link = serializers.CharField(required=False, validators=[YouTubeLinkValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """

    lessons_count = serializers.SerializerMethodField()
    # lessons = LessonSerializer(many=True, required=False)
    lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj: Course) -> int:
        return obj.lessons.count()

    def get_lessons(self, obj: Course) -> list[str]:
        return [lesson.title for lesson in obj.lessons.all()]

    def get_subscription(self, obj: Course) -> bool:
        user = self.context["request"].user
        subscription = CourseSubscription.objects.filter(course=obj, user=user).first()
        print(f"{user=} {obj=} {subscription=}")

        if subscription:
            return True
        else:
            return False


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model
    """

    title = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "user",
            "title",
            "date",
            "amount",
            "course",
            "lesson",
            "method",
        )

    def get_title(self, obj: Payment) -> str:
        if obj.course:
            return obj.course.title
        elif obj.lesson:
            return obj.lesson.title
        return ""


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseSubscription model
    """

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        error_messages={"does_not_exist": "No course with that id"},
    )

    class Meta:
        model = CourseSubscription
        fields = "__all__"
