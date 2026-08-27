from rest_framework import serializers

from lms.models import Course, Lesson, Payment



class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model
    """

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    # lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj: Course) -> int:
        return obj.lessons.count()

    # def get_lessons(self, obj):
    #     return [lesson.title for lesson in obj.lessons.all()]


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