from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the related conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If object is a Message, check its conversation participants
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        # If object is a Conversation
        return user in obj.participants.all()
