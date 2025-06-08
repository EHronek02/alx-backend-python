from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Will add additional fields not present in the default User model
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for the User")
    )
    email = models.EmailField(
        unique=True,
        help_text=_("User's email address")
    )
    password = models.CharField(
        max_length=128,
        help_text=_("User's hashed password")
    )
    first_name = models.CharField(
        max_length=100,
        help_text=_("User's first name")
    )
    last_name = models.CharField(
        max_length=100,
        help_text=_("User's first name")
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text=_("User's phone number")
    )

    REQUIRED_FIELDS = [
        'email',
        'last_name',
        'first_name']

    def __str__(self):
        """String representation for user object"""
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Model representating a conversation between multiple users"""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for the conversation")
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text=_("Users participating in this conversation")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("when conversation was started")
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("last time the conversation object was updated")
    )
    is_group = models.BooleanField(
        default=False,
        help_text=_("Whether this is a group conversation")
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("name of the conversation")
    )

    def __str__(self):
        """Sting representation of the Conversation object"""
        if self.is_group:
            return f"Group: {self.name or ', '.join([u.username for u in self.participants.all()[:3]]) + '...'}"
        participants = self.participants.all()
        return f"Chat between \
            {participants[0]} and {participants[1]}" if len(participants) > 1 \
                else str(self.id) + "." +str(self.name)


class Message(models.Model):
    """Model representing individual messages within
    a conversation"""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for the message")
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text=_("Conversation this message belongs to")
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        help_text=_("User who sent this message")
    )
    message_body = models.TextField(
        help_text=_("The message content")
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the mssage was sent")
    )
    read = models.BooleanField(
        default=False,
        help_text=_("whether message has been read by recipients")
    )

    def __str__(self):
        """String representation for the Message class"""
        return f"{self.sender.username}: {self.message_body[:30]}"