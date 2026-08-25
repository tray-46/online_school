from rest_framework import serializers

from lms.models import Course, Lesson


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
