from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from lms.models import Course, Lesson


# Create your models here.
class User(AbstractUser):
    """
    Represent a service user
    """

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Номер телефона", help_text="Укажите номер телефона"
    )
    city = models.CharField(max_length=35, null=True, blank=True, verbose_name="Город", help_text="Укажите город")
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар", help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """
    represent a payment for course or lesson
    """
    PAYMENT_METHOD_CHOICES = (
        (0, "наличные"),
        (1, "перевод на счёт"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payments", null=True, blank=True, verbose_name="Пользователь",
                             help_text="Выберите пользователя")
    # date = models.DateField(auto_now_add=True)
    # отключение автозаполнения для тестовых данных
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments", null=True, blank=True,
                               verbose_name="Курс", help_text="Выберите курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments", null=True, blank=True,
                               verbose_name="Урок", help_text="Выберите урок")
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты")
    method = models.PositiveSmallIntegerField(choices=PAYMENT_METHOD_CHOICES, default=0, verbose_name="Способ оплаты",
                                              help_text="Выберите способ оплаты")

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def clean(self):
        super().clean()

        if (self.course is None and self.lesson is None) or (self.course and self.lesson):
            raise ValidationError("Choose course or lesson you want to pay")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} payment for {self.course if self.course else self.lesson}"
