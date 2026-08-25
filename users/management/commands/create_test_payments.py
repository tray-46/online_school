from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import Payment

User = get_user_model()

class Command(BaseCommand):
    help = "Create some users for tests"

    def handle(self, *args: Any, **options: Any) -> None:
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user3 = User.objects.get(username="user3")

        payments = list()

        user1_payment_1 = Payment(user=user1, date="2026-08-01", course_id=1, amount=2500, method=1)
        payments.append(user1_payment_1)
        user1_payment_2 = Payment(user=user1, date="2026-08-25", lesson_id=6, amount=500, method=0)
        payments.append(user1_payment_2)
        user1_payment_3 = Payment(user=user1, date="2026-08-26", lesson_id=11, amount=500, method=0)
        payments.append(user1_payment_3)

        user2_payment_1 = Payment(user=user2, date="2026-07-01", lesson_id=6, amount=500, method=1)
        payments.append(user2_payment_1)
        user2_payment_2 = Payment(user=user2, date="2026-07-03", lesson_id=7, amount=500, method=1)
        payments.append(user2_payment_2)
        user2_payment_3 = Payment(user=user2, date="2026-07-06", lesson_id=8, amount=500, method=1)
        payments.append(user2_payment_3)
        user2_payment_4 = Payment(user=user2, date="2026-07-09", lesson_id=9, amount=500, method=1)
        payments.append(user2_payment_4)
        user2_payment_5 = Payment(user=user2, date="2026-07-12", lesson_id=10, amount=500, method=1)
        payments.append(user2_payment_5)

        user3_payment_1 = Payment(user=user3, date="2026-07-01", course_id=5, amount=10000, method=0)
        payments.append(user3_payment_1)
        user3_payment_2 = Payment(user=user3, date="2026-07-03", lesson_id=1, amount=500, method=1)
        payments.append(user3_payment_2)
        user3_payment_3 = Payment(user=user3, date="2026-07-06", lesson_id=6, amount=500, method=1)
        payments.append(user3_payment_3)
        user3_payment_4 = Payment(user=user3, date="2026-07-09", lesson_id=11, amount=500, method=1)
        payments.append(user3_payment_4)
        user3_payment_5 = Payment(user=user3, date="2026-07-12", lesson_id=12, amount=500, method=1)
        payments.append(user3_payment_5)

        payments_counter = 0
        for payment in payments:
            try:
                payment.save()
                payments_counter += 1
            except Exception as e:
                print(e)

        self.stdout.write(self.style.SUCCESS(f"{payments_counter} Payments successfully added"))
