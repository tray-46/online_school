from typing import Any

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import stripe
import unittest
from unittest.mock import patch, MagicMock

import lms.services
from lms.models import Course, CourseSubscription, Lesson, Payment
from users.models import User

from lms.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session


# Create your tests here.
class LessonTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@lms.com", username="user", password="user")
        self.author = User.objects.create(email="author@lms.com", username="author", password="author")

        moderators_group = Group.objects.create(name="Moderators")
        self.moderator = User.objects.create(email="moderator@lms.com", username="moderator", password="moderator")
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            title="test course", description="test course description", author=self.author
        )
        self.lesson = Lesson.objects.create(
            course=self.course, title="test lesson1", description="lesson1 description", price=100, author=self.author
        )

    def test_create_lesson(self) -> None:
        """
        Ensure we can create a new lesson
        """
        url = reverse("lms:lesson_create")

        data = {"course": self.course.pk, "title": "test lesson2", "description": "lesson2 description"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.author)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons(self) -> None:
        url = reverse("lms:lesson_list")
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "course": self.course.pk,
                    "video_link": None,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview_image": None,
                    "author": self.author.pk,
                    "price": 100
                }
            ],
        }
        empty_result: dict[str, Any] = {"count": 0, "next": None, "previous": None, "results": []}

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.author)
        response = self.client.get(url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, empty_result)

    def test_retrieve_lesson(self) -> None:
        url = reverse("lms:lesson_detail", args=[self.lesson.pk])
        result = {
            "id": self.lesson.pk,
            "course": self.course.pk,
            "video_link": None,
            "title": self.lesson.title,
            "description": self.lesson.description,
            "preview_image": None,
            "price": 100,
            "author": self.author.pk,
        }

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.author)
        response = self.client.get(url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson(self) -> None:
        url = reverse("lms:lesson_update", args=[self.lesson.pk])

        data = {
            "title": "test lesson1 updated",
        }

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.author)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), data.get("title"))

        data = {
            "title": "test lesson1 moderated",
        }

        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), data.get("title"))

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson(self) -> None:
        url = reverse("lms:lesson_delete", args=[self.lesson.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.author)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class CourseSubscriptionTest(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(email="user1@lms.com", username="user1", password="user1")
        self.user2 = User.objects.create(email="user2@lms.com", username="user2", password="user2")
        self.author = User.objects.create(email="author@lms.com", username="author", password="author")

        moderators_group = Group.objects.create(name="Moderators")
        self.moderator = User.objects.create(email="moderator@lms.com", username="moderator", password="moderator")
        self.moderator.groups.add(moderators_group)

        self.course = Course.objects.create(
            title="test course", description="test course description", author=self.author
        )
        self.lesson = Lesson.objects.create(
            course=self.course, title="test lesson1", description="lesson1 description", author=self.author
        )
        self.subscription = CourseSubscription.objects.create(user=self.user1, course=self.course)

    def test_subscribe(self) -> None:
        url = reverse("lms:course_subscription", args=[self.course.pk])
        result = {"message": "Подписка добавлена"}

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, result)
        self.assertEqual(CourseSubscription.objects.count(), 2)

    def test_unsubscribe(self) -> None:
        url = reverse("lms:course_subscription", args=[self.course.pk])
        result = {"message": "Подписка удалена"}

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result)
        self.assertEqual(CourseSubscription.objects.count(), 0)


class StripeProductCreationTest(unittest.TestCase):

    @patch("stripe.Product.create")
    def test_create_stripe_product_success(self, mock_product_create):
        mock_product_response = {
            "id": "prod_12345",
            "object": "product",
            "active": True,
            "name": "test product",
        }
        mock_product_create.return_value = mock_product_response

        result = create_stripe_product(product_name="test product")

        mock_product_create.assert_called_once_with(name="test product")

        self.assertEqual(result["id"], "prod_12345")
        self.assertEqual(result["name"], "test product")

    def test_create_stripe_product_missing_name(self):
        with self.assertRaises(ValueError):
            create_stripe_product(product_name="")

    @patch("stripe.Product.create")
    def test_create_stripe_product_stripe_error(self, mock_product_create):
        mock_product_create.side_effect = stripe.error.InvalidRequestError(
            message="Invalid parameters",
            param="name"
        )

        with self.assertRaises(stripe.error.StripeError):
            create_stripe_product(product_name="Bad name")


class StripePriceCreationTest(unittest.TestCase):

    @patch("stripe.Price.create")
    def test_create_price_success(self, mock_price_create):
        mock_product = MagicMock()
        mock_product.id = "prod_12345"

        mock_price_response = {
            "id": "price_12345",
            "object": "price",
            "product": "prod_12345",
            "active": True,
            "unit_amount": 1000,
            "currency": "rub",
        }
        mock_price_create.return_value = mock_price_response

        result = create_stripe_price(
            product=mock_product,
            amount=10,
            currency="rub"
        )

        mock_price_create.assert_called_once_with(product=mock_product.id, unit_amount=1000, currency="rub")
        self.assertEqual(result["id"], "price_12345")
        self.assertEqual(result["product"], mock_product.id)
        self.assertEqual(result["unit_amount"], 1000)

    @patch("stripe.Price.create")
    def test_create_stripe_price_stripe_error(self, mock_price_create):
        mock_product = MagicMock()
        mock_product.id = "prod_12345"

        mock_price_create.side_effect = stripe.error.InvalidRequestError(
            message="Request req_12345: No such product: 'prod_12345'", param="product"
        )

        with self.assertRaises(stripe.error.StripeError):
            create_stripe_price(product=mock_product, amount=10)


class StripeCheckoutSessionCreateTest(unittest.TestCase):

    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session_success(self, mock_session_create):
        mock_price = MagicMock()
        mock_price.id = "price_12345"
        mock_price.unit_amount = 100

        mock_user = MagicMock()
        mock_user.id = 1

        mock_session_response = {
            "id": "cs_12345",
            "object": "checkout.session",
            "mode": "payment",
            "amount_total": 100,
            "status": "open",
            "url": "https://checkout.stripe.com/c/pay/cs_12345",
            "metadata": {
                "user_id": "1"
            },
        }
        mock_session_create.return_value = mock_session_response

        result = create_stripe_checkout_session(mock_price, mock_user.id)

        mock_session_create.assert_called_once_with(
            line_items=[{"price": "price_12345", "quantity": 1, }],
            mode="payment",
            success_url="http://127.0.0.1:8000/payments/{CHECKOUT_SESSION_ID}/",
            cancel_url="http://127.0.0.1:8000/",
            metadata={"user_id": "1"}
        )
        self.assertEqual(result["id"], "cs_12345")
        self.assertEqual(result["metadata"]["user_id"], str(mock_user.id))

    @patch("stripe.checkout.Session.create")
    def test_create_stripe_price_stripe_error(self, mock_session_create):
        mock_price = MagicMock()
        mock_price.id = "price_12345"
        mock_price.unit_amount = 100

        mock_user = MagicMock()
        mock_user.id = 1

        mock_session_create.side_effect = stripe.error.InvalidRequestError(
            message="Request req_12345: No such price: 'price_12345'", param="price"
        )

        with self.assertRaises(stripe.error.StripeError):
            create_stripe_checkout_session(price=mock_price, user_id=mock_user.id)
