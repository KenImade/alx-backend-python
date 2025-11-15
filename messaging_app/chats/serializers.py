from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_email = serializers.EmailField(read_only=True)

    class Meta:
        model = Message
        fields = ("message_id", "sender", "message_body", "sent_at")

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "messages", "created_at")

    def get_participant_count(self, obj):
        return obj.participants.count()