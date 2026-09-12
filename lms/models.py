from typing import Any

from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User


# Create your models here.
class Course(models.Model):
    """
    represents a training course
    """

    title = models.CharField(
        max_length=50, unique=True, verbose_name="Название курса", help_text="Кажите название курса"
    )
    preview_image = models.ImageField(
        upload_to="courses/previews/",
        null=True,
        blank=True,
        verbose_name="Обложка курса",
        help_text="Загрузите изображение",
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание курса", help_text="Укажите описание курса"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="Стоимость")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    """
    represents a lesson
    """

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс", help_text="Выберите курс"
    )
    title = models.CharField(max_length=50, verbose_name="Название урока", help_text="Укажите название урока")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    preview_image = models.ImageField(
        upload_to="lessons/previews/",
        null=True,
        blank=True,
        verbose_name="Обложка урока",
        help_text="Загрузите изображение",
    )
    video_link = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="Стоимость")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:
        return self.title


class Payment(models.Model):
    """
    represent a payment for course or lesson
    """

    PAYMENT_METHOD_CHOICES = (
        (0, "наличные"),
        (1, "перевод на счёт"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )
    date = models.DateField(auto_now_add=True)
    # отключение автозаполнения для тестовых данных
    # date = models.DateField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Урок",
        help_text="Выберите урок",
    )
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты")
    method = models.PositiveSmallIntegerField(
        choices=PAYMENT_METHOD_CHOICES, default=0, verbose_name="Способ оплаты", help_text="Выберите способ оплаты"
    )
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Stripe Product ID")
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Stripe Price ID")
    stripe_checkout_session = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Stripe Checkout Session Id"
    )
    stripe_checkout_url = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="Stripe Checkout Session url"
    )
    status = models.BooleanField(default=False, verbose_name="Payment status")

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def clean(self) -> None:
        super().clean()

        if (self.course is None and self.lesson is None) or (self.course and self.lesson):
            raise ValidationError("Choose course or lesson you want to pay")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} payment for {self.course if self.course else self.lesson}"


class CourseSubscription(models.Model):
    """
    represent a subscription for the course
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["course", "user"],
                name="unique_course_subscription",
                violation_error_message="User already has subscription for this course.",
            )
        ]
