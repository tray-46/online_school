from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


# Create your views here.
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ("course", "lesson", "course__title", "lesson__title", "method")
    ordering_fields = ("date",)
