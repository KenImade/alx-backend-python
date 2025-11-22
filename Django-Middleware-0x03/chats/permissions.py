from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the related conversation. Only participants can send, view, update, delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow only GET, POST, PUT, PATCH, DELETE for participants
        if hasattr(obj, "conversation"):
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return user in obj.conversation.participants.all()
        elif hasattr(obj, "participants"):
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return user in obj.participants.all()

        return False
