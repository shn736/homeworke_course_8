from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import Subscription, User


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.user
        )
        self.subscribe_url = reverse("users:subscribe")

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.subscribe_url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        subscription_exists = Subscription.objects.filter(
            subscription_user=self.user, subscription_course=self.course
        ).exists()
        self.assertTrue(subscription_exists)

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)

        Subscription.objects.create(
            subscription_user=self.user, subscription_course=self.course
        )

        response = self.client.post(self.subscribe_url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")

        subscription_exists = Subscription.objects.filter(
            subscription_user=self.user, subscription_course=self.course
        ).exists()
        self.assertFalse(subscription_exists)

    def test_subscribe_to_non_existent_course(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.subscribe_url, {"course_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
