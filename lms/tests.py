from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, CourseSubscription
from users.models import User
from django.contrib.auth.models import Group


# Create your tests here.
class LessonTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@lms.com", username="user", password="user")
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

    def test_create_lesson(self):
        """
        Ensure we can create a new lesson
        """
        url = reverse("lms:lesson_create")

        data = {
            "course": self.course.pk,
            "title": "test lesson2",
            "description": "lesson2 description"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.author)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons(self):
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
                }
            ]
        }
        empty_result = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
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
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, empty_result)

    def test_retrieve_lesson(self):
        url = reverse("lms:lesson_detail", args=[self.lesson.pk])
        result = {
            "id": self.lesson.pk,
            "course": self.course.pk,
            "video_link": None,
            "title": self.lesson.title,
            "description": self.lesson.description,
            "preview_image": None,
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

    def test_update_lesson(self):
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

    def test_delete_lesson(self):
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

    def setUp(self):
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

    def test_subscribe(self):
        url = reverse("lms:course_subscription", args=[self.course.pk])
        result = {"message": "Подписка добавлена"}

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, result)
        self.assertEqual(CourseSubscription.objects.count(), 2)

    def test_unsubscribe(self):
        url = reverse("lms:course_subscription", args=[self.course.pk])
        result = {"message": "Подписка удалена"}

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, result)
        self.assertEqual(CourseSubscription.objects.count(), 0)
