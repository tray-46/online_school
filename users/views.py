from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
