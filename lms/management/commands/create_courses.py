from typing import Any

from django.core.management.base import BaseCommand

from lms.models import Course


class Command(BaseCommand):
    help = "Create some courses for tests"

    def handle(self, *args: Any, **options: Any) -> None:
        python_course, _ = Course.objects.get_or_create(title="python", description="python for beginners")
        java_course, _ = Course.objects.get_or_create(title="java", description="java for beginners")
        odin_s_course, _ = Course.objects.get_or_create(title="1С программист", description="1C like a pro")
        tester_course, _ = Course.objects.get_or_create(title="Инженер по тестированию", description="QA")
        cyber_sec_course, _ = Course.objects.get_or_create(title="Специалист по кибербезопасности", description="CB<")

        self.stdout.write(self.style.SUCCESS("Courses successfully added"))
