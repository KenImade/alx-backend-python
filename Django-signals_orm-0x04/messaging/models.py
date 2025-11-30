from django.db import models
from django.contrib.auth.models import User


# --- Message Model ---
class Message(models.Model):
    # The sender of the message
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )

    # The receiver of the message
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )

    # Field for Threading
    parent_message = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    # The current content of the message
    content = models.TextField()

    # The timestamp when the message was initially created
    timestamp = models.DateTimeField(auto_now_add=True)

    # Tracks if the message has ever been edited
    edited = models.BooleanField(default=False)

    # 🌟 NEW FIELD: Tracks if the receiver has read the message
    read = models.BooleanField(default=False)

    # 🌟 Custom Managers
    objects = models.Manager()  # The default manager
    unread = UnreadMessagesManager()  # The custom manager for unread messages

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        status = "(Read)" if self.read else "(Unread)"
        return f"From {self.sender.username} to {self.receiver.username} {status}"


# --- MessageHistory Model (NEW) ---
class MessageHistory(models.Model):
    # Link to the Message that was edited
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )

    # Store the content *before* the current edit
    old_content = models.TextField()

    # The time of the edit
    edited_at = models.DateTimeField(auto_now=True)

    # The user who performed the edit (usually the sender)
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="message_edited_by"
    )

    class Meta:
        ordering = ["-edited_at"]
        verbose_name = "Message History"
        verbose_name_plural = "Message History"

    def __str__(self):
        return f"History for Message {self.message.id} recorded at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"


# --- Notification Model (Optional inclusion for completeness) ---
class Notification(models.Model):
    # ... (Content remains the same as previous response)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"
