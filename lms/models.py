from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview_image = models.ImageField(
        upload_to="lms/course_previews",
        verbose_name="Превью",
        help_text="Загрузите превью",
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=100, verbose_name="Описание", help_text="Введите описание"
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите пользователя",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        max_length=100, verbose_name="Описание", help_text="Введите описание"
    )
    preview_image = models.ImageField(
        upload_to="lms/lesson_previews",
        verbose_name="Превью",
        help_text="Загрузите превью",
        blank=True,
        null=True,
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Введите курс",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите пользователя",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
