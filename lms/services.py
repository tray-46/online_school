# import os
# import django
#
# # Replace 'your_project_name' with the folder name containing your settings.py
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()

import stripe
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core import mail

from config.settings import STRIPE_CHECKOUT_CANCEL_URL, STRIPE_CHECKOUT_SUCCESS_URL, STRIPE_SECRET_KEY
from lms.models import CourseSubscription

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(product_name: str) -> stripe.Product:
    if not product_name:
        raise ValueError("Product name is required")

    try:
        stripe_product = stripe.Product.create(name=product_name)
        return stripe_product
    except stripe.error.StripeError as e:
        raise e


def create_stripe_price(product: stripe.Product, amount: float, currency: str = "rub") -> stripe.Price:
    unit_amount = int(amount * 100)

    try:
        stripe_price = stripe.Price.create(
            product=product.id,
            unit_amount=unit_amount,
            currency=currency,
        )
        return stripe_price
    except stripe.error.StripeError as e:
        raise e


def create_stripe_checkout_session(price: stripe.Price, user_id: int) -> stripe.checkout.Session:

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=STRIPE_CHECKOUT_SUCCESS_URL,
            cancel_url=STRIPE_CHECKOUT_CANCEL_URL,
            metadata={
                "user_id": str(user_id),
            },
        )
        return checkout_session
    except stripe.error.StripeError as e:
        raise e


def get_stripe_checkout_session_info(session_id: str) -> stripe.checkout.Session:
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        return checkout_session
    except stripe.error.StripeError as e:
        raise e


def send_course_update_notification(course_id: int) -> None:
    subscribers = CourseSubscription.objects.filter(course_id=course_id).select_related("course", "user")

    messages = list()
    for subscriber in subscribers:
        msg = mail.EmailMessage(
            subject=f"Course '{subscriber.course.title}' Updated",
            body="You receive this message because course you subscribe for was updated./n/nКоманда sky.school.com",
            from_email=DEFAULT_FROM_EMAIL,
            to=[
                subscriber.user.email,
            ],
        )
        messages.append(msg)

    if messages:
        backend = mail.mailers.default
        backend.send_messages(messages)


if __name__ == "__main__":
    # test_product = create_stripe_product("test product")
    # print(test_product)
    # product_price = create_stripe_price(test_product, 100)
    # print(product_price)
    # session = create_stripe_checkout_session(product_price, 1)
    # print(session)
    # session = get_stripe_checkout_session_info(session_id="cs_123")
    # print(session)
    # send_course_update_notification(1)
    pass
