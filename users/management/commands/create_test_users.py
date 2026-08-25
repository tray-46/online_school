from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = "Create some users for tests"

    def handle(self, *args: Any, **options: Any) -> None:
        user1 = User(email="user1@sky.school.com", username="user1")
        user1.set_password("user1")
        user2 = User(email="user2@sky.school.com", username="user2")
        user2.set_password("user2")
        user3 = User(email="user3@sky.school.com", username="user3")
        user3.set_password("user3")

        try:
            User.objects.bulk_create([user1, user2, user3])
            self.stdout.write(self.style.SUCCESS("Users successfully added"))
        except Exception as e:
            print(e)
