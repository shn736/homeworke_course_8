from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import UrlValidator
from users.models import Subscription


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_link")]


class CourseDetailSerializer(serializers.ModelSerializer):

    count_lesson_with_same_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_count_lesson_with_same_course(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):  # Метод для проверки подписки
        user = self.context["request"].user
        return Subscription.objects.filter(
            subscription_course=obj, subscription_user=user
        ).exists()

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "count_lesson_with_same_course",
            "lessons",
            "owner",
            "is_subscribed",
        ]
        validators = [UrlValidator(field="description")]
