from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):

    def has_permission(self, request,view):
        return bool(request.user.groups.filter(name="Moderators").exists())

    def has_object_permission(self, request, view, obj):
        return bool(request.user.groups.filter(name="Moderators").exists())
