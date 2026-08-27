from typing import Any

from django.core.management.base import BaseCommand

from lms.models import Lesson


class Command(BaseCommand):
    help = "Create some lessons for tests"

    def handle(self, *args: Any, **options: Any) -> None:
        python_1, _ = Lesson.objects.get_or_create(
            title="Знакомство с Python",
            description="Напишем вашу первую программу - Hello, Python World!",
            preview_image="lessons/previews/py_l1_QmlRYf6.png",
            video_link="=Pc9MvZkHlMa",
            course_id=1,
            author=1
        )
        python_2, _ = Lesson.objects.get_or_create(title="Типы данных", course_id=1, author=1)
        python_3, _ = Lesson.objects.get_or_create(title="Циклы", course_id=1, author=1)
        python_4, _ = Lesson.objects.get_or_create(title="Математические операции", course_id=1, author=1)
        python_5, _ = Lesson.objects.get_or_create(title="Функции", course_id=1, author=1)

        java_1, _ = Lesson.objects.get_or_create(
            title="Знакомство с Java", description="Напишем вашу первую программу - Hello, Java World!", course_id=2, author=9
        )
        java_2, _ = Lesson.objects.get_or_create(title="Переменные. Вывод и ввод данных", course_id=2, author=9)
        java_3, _ = Lesson.objects.get_or_create(title="Математические операции", course_id=2, author=9)
        java_4, _ = Lesson.objects.get_or_create(title="Условная конструкция. Оператор if", course_id=2, author=9)
        java_5, _ = Lesson.objects.get_or_create(title="Циклы while и for. Вложенные циклы", course_id=2, author=9)

        odin_s_1, _ = Lesson.objects.get_or_create(title="Что такое 1C", course_id=3, author=10)

        tester_1, _ = Lesson.objects.get_or_create(title="Что такое разработка ПО", course_id=4, author=1)
        tester_2, _ = Lesson.objects.get_or_create(title="Кто участвует в процессе разработки", course_id=4, author=1)
        tester_3, _ = Lesson.objects.get_or_create(title="Как выстроить эффективную работу", course_id=4, author=1)
        tester_4, _ = Lesson.objects.get_or_create(title="Что такое качественное ПО", course_id=4, author=1)
        tester_5, _ = Lesson.objects.get_or_create(title="Что такое QA", course_id=4, author=1)
        tester_6, _ = Lesson.objects.get_or_create(title="Чем занимаются QA-инженеры ", course_id=4, author=1)
        tester_7, _ = Lesson.objects.get_or_create(title="Виды тестирования", course_id=4, author=1)
        tester_8, _ = Lesson.objects.get_or_create(title="7 принципов тестирования", course_id=4, author=1)
        tester_9, _ = Lesson.objects.get_or_create(title="Что нужно, чтобы стать QA-инженером", course_id=4, author=1)

        cyber_sec_1, _ = Lesson.objects.get_or_create(title="Введение в Linux", course_id=5, author=11)
        cyber_sec_2, _ = Lesson.objects.get_or_create(title="Первая установка Linux", course_id=5, author=11)
        cyber_sec_3, _ = Lesson.objects.get_or_create(title="Структура ОС Linux", course_id=5, author=11)
        cyber_sec_4, _ = Lesson.objects.get_or_create(title="Знакомство с терминалом", course_id=5, author=11)
        cyber_sec_5, _ = Lesson.objects.get_or_create(title="Устройства в Linux", course_id=5, author=11)
        cyber_sec_6, _ = Lesson.objects.get_or_create(title="Диски и файловые системы", course_id=5, author=11)
        cyber_sec_7, _ = Lesson.objects.get_or_create(title="Устройство файловых сисВведение в Linux", course_id=5, author=11)
        cyber_sec_8, _ = Lesson.objects.get_or_create(title="Первая установка Linux", course_id=5, author=11)
        cyber_sec_9, _ = Lesson.objects.get_or_create(title="Структура ОС Linux", course_id=5, author=11)

        self.stdout.write(self.style.SUCCESS("Lessons successfully added"))
