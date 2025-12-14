from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ModelSerializer

from users.models import Payment, Subscription, User
from users.services import process_payment


class PaymentSerializer(ModelSerializer):
    filterset_fields = ["course", "lesson", "payment_method"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["payment_date"]

    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):
        payment_response = process_payment(validated_data)
        return payment_response


class UserSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
