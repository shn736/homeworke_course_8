from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from users.models import Payment, Subscription, User
from users.serializer import PaymentSerializer, UserSerializer


class PaymentCreateApiView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_response = serializer.save()
            return Response(payment_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveApiView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(
            subscription_user=user, subscription_course=course_item
        )

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"

        else:
            Subscription.objects.create(
                subscription_user=user, subscription_course=course_item
            )
            message = "подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
