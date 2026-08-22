from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model
    """
    class Meta:
        model = Lesson
        fields = '__all__'
