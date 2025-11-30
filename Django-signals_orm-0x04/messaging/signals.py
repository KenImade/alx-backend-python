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


from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_history_on_edit(sender, instance, **kwargs):
    """
    Listens for a Message instance about to be saved (updated) and logs
    its previous content into the MessageHistory model.
    """
    # Check if this instance already exists in the database (i.e., it's an update, not a creation)
    if instance.pk:
        try:
            # Get the current version of the object from the database
            old_message = Message.objects.get(pk=instance.pk)

            # Check if the content has actually changed
            if old_message.content != instance.content:

                # 1. Log the previous content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    # We assume the editor is the original sender for simplicity
                    # in this model-only example. In a real view, you'd pass
                    # the request.user to save() or the signal.
                    editor=instance.sender,
                )

                # 2. Update the 'edited' field on the Message instance before it's saved
                instance.edited = True

                print(
                    f"--- PRE_SAVE: Content change detected for Message {instance.pk}. Old content logged. ---"
                )

        except ObjectDoesNotExist:
            # This should generally not happen if pk exists, but good practice to catch
            print(f"--- Warning: Object {instance.pk} not found during pre_save. ---")
    else:
        # This is a new message creation, do nothing.
        print(f"--- PRE_SAVE: New Message creation. Skipping history log. ---")
