from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import Payment, Subscription, User


class PaymentSerializer(ModelSerializer):
    filterset_fields = ["course", "lesson", "payment_method"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["payment_date"]

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
