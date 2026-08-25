import io

from typing import Any

from django.core.management.color import no_style
from django.db import connection
from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = "Fill database with test data"

    def handle(self, *args: Any, **options: Any) -> None:
        call_command("create_test_users")

        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # output_buffer = io.StringIO()
        # call_command("sqlsequencereset", "lms", stdout=output_buffer, no_color=True)
        # captured_data = output_buffer.getvalue()
        # call_command("dbshell", parameters=["-c", captured_data])

        sequence_reset_sql = connection.ops.sequence_reset_sql(no_style(), [Lesson, Payment, Course])
        with connection.cursor() as cursor:
            for sql in sequence_reset_sql:
                cursor.execute(sql)

        call_command("create_courses")
        call_command("create_lessons")
        call_command("create_test_payments")

        self.stdout.write(self.style.SUCCESS("Database successfully filled with test data"))
