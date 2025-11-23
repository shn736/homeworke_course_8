from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, filters
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    filterset_fields = ["course", "lesson", "payment_method"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['payment_date']

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone", "city", "payment")
