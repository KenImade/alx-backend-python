from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
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


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Cleans up all remaining Message, Notification, and MessageHistory records
    associated with a User *after* the User account has been deleted.

    NOTE: With proper on_delete=CASCADE settings on Foreign Keys, this manual
    cleanup is often redundant for many relations, but it ensures all related
    objects are handled, especially for complex or multi-step relations.
    """
    user_id = instance.pk  # The PK of the deleted user is still available here

    # 1. Delete Messages: Delete messages sent/received by the deleted user.
    #    (This is usually handled by CASCADE, but performed manually here for the signal objective)
    messages_to_delete = Message.objects.filter(
        models.Q(sender_id=user_id) | models.Q(receiver_id=user_id)
    )
    deleted_messages_count, _ = messages_to_delete.delete()
    print(
        f"--- POST_DELETE: Deleted {deleted_messages_count} Messages for user {user_id}. ---"
    )

    # 2. Delete Notifications: Notifications where the user was the recipient.
    #    (This is usually handled by CASCADE on Notification.user)
    deleted_notifications_count, _ = Notification.objects.filter(
        user_id=user_id
    ).delete()
    print(
        f"--- POST_DELETE: Deleted {deleted_notifications_count} Notifications for user {user_id}. ---"
    )

    # 3. Clean up orphaned Message History records related to the deleted user's messages.
    #    If a Message is deleted (step 1), its related MessageHistory records will
    #    be deleted due to CASCADE on MessageHistory.message.

    # We can perform a safety check for any remaining MessageHistory records
    # where the editor was the deleted user (only if MessageHistory.editor was CASCADE)
    # Since we set MessageHistory.editor to SET_NULL, no further action is required for the editor field.

    print(
        f"--- Signal Triggered: Cleanup complete for deleted user: {instance.username} ---"
    )
