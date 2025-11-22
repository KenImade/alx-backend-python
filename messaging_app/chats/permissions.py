from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Allow users to access only their own messages/conversations."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
