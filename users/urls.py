from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("users/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user_update"),
]
