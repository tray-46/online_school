from celery import shared_task

from lms.services import send_course_update_notification


@shared_task
def course_update_notification_task(course_id: int) -> None:
    send_course_update_notification(course_id)
