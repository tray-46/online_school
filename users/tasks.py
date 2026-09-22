from celery import shared_task

from users.services import block_inactive_users


@shared_task
def block_inactive_users_task() -> None:
    block_inactive_users()
