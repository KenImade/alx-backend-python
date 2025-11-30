from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageSignalTest(TestCase):
    """
    Tests for the signal that creates a Notification upon new Message creation.
    """

    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username="alice", password="password")
        self.user2 = User.objects.create_user(username="bob", password="password")

        # Ensure there are no notifications initially
        Notification.objects.all().delete()

    def test_notification_created_on_new_message(self):
        """
        Test that creating a new Message automatically generates a Notification
        for the receiver.
        """
        # 1. Assert there are no notifications before creating the message
        self.assertEqual(Notification.objects.count(), 0)

        # 2. Create a new message from user1 to user2
        message_content = "Hello Bob, how are you?"
        new_message = Message.objects.create(
            sender=self.user1, receiver=self.user2, content=message_content
        )

        # 3. Assert that a single notification has been created
        self.assertEqual(Notification.objects.count(), 1)

        # 4. Retrieve the newly created notification
        notification = Notification.objects.first()

        # 5. Assert the notification details are correct
        self.assertEqual(
            notification.user, self.user2
        )  # Notification is for the receiver
        self.assertEqual(notification.message, new_message)
        self.assertIn("You have a new message from alice", notification.content)
        self.assertFalse(notification.is_read)  # Should be unread by default

    def test_no_notification_on_message_update(self):
        """
        Test that updating an existing Message does NOT create a new Notification.
        """
        # Create initial message
        initial_message = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Initial content"
        )
        self.assertEqual(
            Notification.objects.count(), 1
        )  # Initial notification created

        # Update the existing message
        initial_message.content = "Updated content"
        initial_message.save()  # This save should pass 'created=False' to the signal

        # Assert that no new notification was created
        self.assertEqual(Notification.objects.count(), 1)

        # Cleanup
        initial_message.delete()
