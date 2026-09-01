from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as TOPView
from rest_framework_simplejwt.views import TokenRefreshView as TRView

from users.models import User
from users.permissions import IsAccountOwner
from users.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserSerializer,
)


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self) -> type[BaseSerializer]:
        user_profile = self.get_object()
        user = self.request.user
        if user_profile == user:
            return UserDetailSerializer
        return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    parser_classes = [MultiPartParser, FormParser]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAccountOwner]


class TokenObtainPairView(TOPView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)  # type: ignore[assignment]


class TokenRefreshView(TRView):
    serializer_class = TokenRefreshSerializer
    permission_classes = (AllowAny,)  # type: ignore[assignment]
