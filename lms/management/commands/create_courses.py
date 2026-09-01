from typing import Any

from django.core.management.base import BaseCommand

from lms.models import Course


class Command(BaseCommand):
    help = "Create some courses for tests"

    def handle(self, *args: Any, **options: Any) -> None:
        python_course, _ = Course.objects.get_or_create(title="python", description="python for beginners", author=1)
        java_course, _ = Course.objects.get_or_create(title="java", description="java for beginners", author=9)
        odin_s_course, _ = Course.objects.get_or_create(title="1С программист", description="1C like a pro", author=10)
        tester_course, _ = Course.objects.get_or_create(title="Инженер по тестированию", description="QA", author=1)
        cyber_sec_course, _ = Course.objects.get_or_create(
            title="Специалист по кибербезопасности", description="CB<", author=11
        )

        self.stdout.write(self.style.SUCCESS("Courses successfully added"))
