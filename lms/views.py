from typing import Sequence

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, _SupportsHasPermission
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Payment
from lms.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.permissions import IsAuthor, IsModerator


# Create your views here.
class CourseViewSet(ModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsAuthor]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsAuthor]

        return super().get_permissions()

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(author=self.request.user)

    def get_queryset(self) -> QuerySet[Course]:
        is_moderator = IsModerator()
        if is_moderator.has_permission(self.request, self):
            return Course.objects.all()
        elif self.request.user.is_authenticated:
            return Course.objects.filter(author=self.request.user)
        return Course.objects.none()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(author=self.request.user)


class LessonListAPIView(ListAPIView):
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAuthor]

    def get_queryset(self) -> QuerySet[Lesson]:
        is_moderator = IsModerator()
        if is_moderator.has_permission(self.request, self):
            return Lesson.objects.all()
        elif self.request.user.is_authenticated:
            return Lesson.objects.filter(author=self.request.user)
        return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAuthor]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAuthor]
    parser_classes = [MultiPartParser, FormParser]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator, IsAuthor]


class PaymentListAPIView(ListAPIView):
    # queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    )
    search_fields = (
        "course__title",
        "lesson__title",
        "method",
        "date",
    )
    ordering_fields = ("date",)
    filterset_fields = ("course", "lesson", "course__title", "lesson__title", "method")

    def get_queryset(self) -> QuerySet[Payment]:
        if self.request.user.is_authenticated:
            return Payment.objects.filter(user=self.request.user)
        return Payment.objects.none()
