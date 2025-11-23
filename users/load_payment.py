import json

from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Загрузите платежи из JSON file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к JSON файлу.")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        with open(file_path) as json_file:
            payment_data = json.load(json_file)
            for data in payment_data:
                user = User.objects.get(
                    pk=data["payment_user"]
                )  # Убедитесь, что пользователь существует
                course = (
                    Course.objects.get(pk=data["payment_course"])
                    if data["payment_course"] is not None
                    else None
                )
                lesson = (
                    Lesson.objects.get(pk=data["payment_lesson"])
                    if data["payment_lesson"] is not None
                    else None
                )

                payment = Payment(
                    payment_user=user,
                    payment_date=data["payment_date"],
                    payment_course=course,
                    payment_lesson=lesson,
                    amount=data["amount"],
                    payment_method=data["payment_method"],
                )
                payment.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Payment {payment.id} successfully created.")
                )
