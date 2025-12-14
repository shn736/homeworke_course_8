import stripe

from config.settings import STRIPE_API_KEY
from lms.models import Course
from users.models import Payment

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course: Course):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(
        name=course.name,
        description=course.description,
        images=[course.preview_image.url] if course.preview_image else [],
    )
    return product


def create_stripe_price(product_id: str, amount: float):
    """Создание цены для продукта в Stripe."""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency="rub",
        recurring=None,
        product=product_id,
    )
    return price


def create_payment_session(price_id: str, success_url: str, cancel_url: str):
    """Создание сессии платёжной в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def process_payment(payment_data):
    """Обработка платежа и создание записи в базе данных."""
    course = payment_data.get("payment_course")
    lesson = payment_data.get("payment_lesson")
    amount = payment_data.get("amount")

    product = create_stripe_product(course)
    price = create_stripe_price(product.id, amount)

    session = create_payment_session(
        price.id, "http://127.0.0.1:8000/", "http://127.0.0.1:8000/"
    )

    payment = Payment.objects.create(
        payment_date=payment_data.get("payment_date"),
        payment_course=course,
        payment_lesson=lesson,
        amount=amount,
        payment_method=payment_data.get("payment_method"),
    )

    payment.stripe_session_url = session.url
    payment.save()

    return {"session_url": session.url, "payment_id": payment.id}
