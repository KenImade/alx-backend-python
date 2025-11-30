from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    # The sender of the message
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )

    # The receiver of the message
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )

    # The content of the message
    content = models.TextField()

    # The timestamp when the message was created
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Notification(models.Model):
    # The user who receives the notification
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    # The message that triggered this notification
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )

    # The notification content
    content = models.CharField(max_length=255)

    # Whether the notification has been read
    is_read = models.BooleanField(default=False)

    # The timestamp when the notification was created
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        read_status = "Read" if self.is_read else "Unread"
        return f"Notification for {self.user.username}: {self.content} ({read_status})"
