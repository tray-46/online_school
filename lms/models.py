from django.db import models


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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:
        return self.title
