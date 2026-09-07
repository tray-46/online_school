from typing import Any, Sequence

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, CourseSubscription, Lesson, Payment
from lms.paginators import Paginator
from lms.serializers import CourseSerializer, CourseSubscriptionSerializer, LessonSerializer, PaymentSerializer, \
    SubscribedSerializer, UnsubscribedSerializer
from users.permissions import IsAuthor, IsModerator
from lms.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session, \
    get_stripe_checkout_session_info


# Create your views here.
class CourseViewSet(ModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Paginator
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self) -> Sequence:
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
            return Course.objects.all().order_by("id")
        elif self.request.user.is_authenticated:
            return Course.objects.filter(author=self.request.user).order_by("id")
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
    pagination_class = Paginator
    permission_classes = [IsAuthenticated, IsModerator | IsAuthor]

    def get_queryset(self) -> QuerySet[Lesson]:
        is_moderator = IsModerator()
        if is_moderator.has_permission(self.request, self):
            return Lesson.objects.all().order_by("id")
        elif self.request.user.is_authenticated:
            return Lesson.objects.filter(author=self.request.user).order_by("id")
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


@extend_schema(
    request=None,
    responses={204: None},
    description="Delete the specifies lesson."
)
class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator, IsAuthor]


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        course = None
        lesson = None
        title = ""
        amount = 0

        if "courses" in self.request.path:
            course = get_object_or_404(Course, pk=self.kwargs.get("pk"))
            title = course.title
            amount = course.price

        if "lessons" in self.request.path:
            lesson = course = get_object_or_404(Lesson, pk=self.kwargs.get("pk"))
            title = lesson.title
            amount = lesson.price

        product = create_stripe_product(title)
        price = create_stripe_price(product, amount)
        checkout_session = create_stripe_checkout_session(price, user.id)

        payment = serializer.save(user=self.request.user, course=course, lesson=lesson, amount=amount)
        payment.stripe_checkout_session = checkout_session.id
        payment.stripe_checkout_url = checkout_session.url
        payment.save()


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


class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self) -> QuerySet[Payment]:
        if self.request.user.is_authenticated:
            return Payment.objects.filter(user=self.request.user)
        return Payment.objects.none()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data

        stripe_session = get_stripe_checkout_session_info(instance.stripe_checkout_session)
        data["stripe_session"] = stripe_session.to_dict(recursive=True)

        return Response(data)


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, ~IsModerator]

    @extend_schema(
        summary="lms_course_subscription",
        description="Processing course subscription: add or delete users subscription for specified course.",
        request=None,
        responses={
            200: UnsubscribedSerializer,
            201: SubscribedSerializer,
        },
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = self.request.user

        if not user or not user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED
            )

        course_id = self.kwargs.get("pk")
        subscription = CourseSubscription.objects.filter(course=course_id, user=user).first()

        if subscription:
            subscription.delete()
            message = "Подписка удалена"
            return Response({"message": message}, status=status.HTTP_200_OK)

        serializer = CourseSubscriptionSerializer(data={"user": user.pk, "course": course_id})
        if serializer.is_valid():
            serializer.save()
            message = "Подписка добавлена"
            return Response({"message": message}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
