from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Укажите страну",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateField()
    payment_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True
    )
    payment_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True
    )
    payment_method = models.CharField(
        max_length=20, choices=[("cash", "Наличные"), ("transfer", "Перевод на счет")]
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите Id сессии",
    )
    stripe_session_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    subscription_user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
