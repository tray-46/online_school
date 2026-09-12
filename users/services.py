# import os
# import django
#
# # Replace 'your_project_name' with the folder name containing your settings.py
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()

from django.utils import timezone
from datetime import timedelta

from users.models import User


def block_inactive_users(days_inactive:int = 30):
    last_login = timezone.now() - timedelta(days=days_inactive)
    User.objects.filter(last_login__lt=last_login).update(is_active=False)


if __name__ == "__main__":
    # block_inactive_users()
    pass