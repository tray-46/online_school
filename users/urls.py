from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("users/register/", views.UserCreateAPIView.as_view(), name="user_register"),
    path("users/", views.UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", views.UserDestroyAPIView.as_view(), name="user_delete"),



    path("payments/", views.PaymentListAPIView.as_view(), name="payments_list"),
]
