from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.contrib.auth.models import User


# This decorator registers the function as a receiver for the post_save signal
# It listens specifically for saves on the Message model.
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Creates a Notification instance for the message receiver when a new Message is created.
    """
    # The 'created' argument is True if a new record was created (not updated)
    if created:
        # Get the receiver user object
        receiver_user = instance.receiver

        # Define the notification message content
        notification_content = (
            f"You have a new message from {instance.sender.username}: "
            f"'{instance.content[:30]}...'"
        )

        # Create and save the new Notification
        Notification.objects.create(
            user=receiver_user,
            message=instance,
            content=notification_content,
        )
        print(f"--- Notification created for {receiver_user.username} ---")


# Note: The signals must be connected when the app is ready, which is done in apps.py
