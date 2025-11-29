from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    count_lesson_with_same_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson_with_same_course(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "count_lesson_with_same_course",
            "lessons",
            "owner",
        ]
