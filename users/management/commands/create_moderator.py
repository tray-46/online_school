from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Create moderators group"

    def handle(self, *args: Any, **options: Any) -> None:
        moderators_group, _ = Group.objects.get_or_create(name="Moderators")

        moderator, _ = User.objects.get_or_create(email="moderator@sku.school.com", username="moderator",
                                               password="moderator")
        moderator.set_password(moderator.password)
        moderator.groups.add(moderators_group)
        moderator.save()

        self.stdout.write(self.style.SUCCESS(f"Moderator successfully added"))
