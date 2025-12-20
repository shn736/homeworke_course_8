from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import Subscription, User


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(subscription_course=course)

    for subscription in subscriptions:
        send_mail(
            subject=f"Обновление курса: {course.name}",
            message="Курс был обновлен. Проверьте обновления на сайте.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.subscription_user.email],
        )


@shared_task
def deactivate_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

    return f"Заблокировано {inactive_users.count()} пользователей."
