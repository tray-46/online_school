from django.db.models import Model
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from lms.models import Course, Lesson


class IsModerator(BasePermission):

    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        return bool(request.user.groups.filter(name="Moderators").exists())

    def has_object_permission(self, request: HttpRequest, view: APIView, obj: Model) -> bool:
        return bool(request.user.groups.filter(name="Moderators").exists())


class IsAuthor(BasePermission):

    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request: HttpRequest, view: APIView, obj: Course | Lesson) -> bool:
        return bool(request.user.is_authenticated and obj.author == request.user)


class IsAccountOwner(BasePermission):

    def has_object_permission(self, request: HttpRequest, view: APIView, obj: Model) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
