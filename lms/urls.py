from django.urls import include, path
from rest_framework.routers import SimpleRouter

from lms import views
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r"courses", views.CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    path("courses/<int:pk>/subscription/", views.CourseSubscriptionAPIView.as_view(), name="course_subscription"),
    path("courses/<int:pk>/buy/", views.PaymentCreateAPIView.as_view(), name="course_buy"),
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/", views.LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/<int:pk>/update/", views.LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", views.LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("payments/", views.PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", views.PaymentRetrieveAPIView.as_view(), name="payments_detail"),
    path("payments/webhook/", views.stripe_webhook, name="stripe_webhook"),
]
