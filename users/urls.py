from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import (PaymentCreateApiView, PaymentDestroyApiView,
                         PaymentListApiView, PaymentRetrieveApiView,
                         PaymentUpdateApiView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("payment/", PaymentListApiView.as_view(), name="payment_list"),
    path(
        "payment/<int:pk>/", PaymentRetrieveApiView.as_view(), name="payment_retrieve"
    ),
    path("payment/create/", PaymentCreateApiView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/delete/",
        PaymentDestroyApiView.as_view(),
        name="payment_delete",
    ),
    path(
        "payment/<int:pk>/update/",
        PaymentUpdateApiView.as_view(),
        name="payment_update",
    ),
]

urlpatterns += router.urls
