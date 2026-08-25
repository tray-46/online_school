from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


# Create your views here.
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter,)
    search_fields = ("course__title", "lesson__title", "method", "date",)
    ordering_fields = ("date",)
    filterset_fields = ("course", "lesson", "course__title", "lesson__title", "method")
