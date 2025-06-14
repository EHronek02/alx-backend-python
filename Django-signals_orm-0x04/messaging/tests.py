from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessageSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='testpass123')
        self.receiver = User.objects.create_user(username='receiver', password='testpass123')

    def test_notification_created_on_new_message(self):
        initial_count = Notification.objects.count()

        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Workd'
        )

        self.assertEqual(Notification.objects.count(), initial_count + 1)

        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.is_read)
