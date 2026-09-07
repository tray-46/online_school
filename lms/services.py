import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(product_name: str) -> stripe.Product:
    stripe_product = stripe.Product.create(
        name=product_name
    )

    return stripe_product


def create_stripe_price(product: stripe.Product, amount: float) -> stripe.Price:
    unit_amount = int(amount * 100)
    stripe_price = stripe.Price.create(
        product=product,
        unit_amount=unit_amount,
        currency="rub",
    )

    return stripe_price


def create_stripe_checkout_session(price: stripe.Price, user_id: int) -> stripe.checkout.Session:
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.STRIPE_CHECKOUT_SUCCESS_URL,
        cancel_url=settings.STRIPE_CHECKOUT_CANCEL_URL,
        metadata={
            "user_id": user_id,
        }
    )

    return checkout_session


def get_stripe_checkout_session_info(session_id) -> stripe.checkout.Session:
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    return checkout_session


if __name__ == "__main__":
    test_product = create_stripe_product("test product")
    product_price = create_stripe_price(test_product, 100)
    session = create_stripe_checkout_session(product_price, 2)
    print(session)
