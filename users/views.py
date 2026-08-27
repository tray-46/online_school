from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView as TOPView, TokenRefreshView as TRView

from lms.models import Payment
from lms.serializers import PaymentSerializer
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer, TokenObtainPairSerializer, \
    TokenRefreshSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: UserCreateSerializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class TokenObtainPairView(TOPView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)


class TokenRefreshView(TRView):
    serializer_class = TokenRefreshSerializer
    permission_classes = (AllowAny,)


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
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
