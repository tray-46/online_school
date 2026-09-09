import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


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
            success_url=settings.STRIPE_CHECKOUT_SUCCESS_URL,
            cancel_url=settings.STRIPE_CHECKOUT_CANCEL_URL,
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


if __name__ == "__main__":
    # test_product = create_stripe_product("test product")
    # print(test_product)
    # product_price = create_stripe_price(test_product, 100)
    # print(product_price)
    # session = create_stripe_checkout_session(product_price, 1)
    # print(session)
    # session = get_stripe_checkout_session_info(session_id="cs_123")
    # print(session)
    pass
