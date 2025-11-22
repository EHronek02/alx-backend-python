from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Will add additional fields not present in the default User Model
    """
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    password_hash = models.CharField(max_length=255)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTImeField(default=timezone.now)

    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['conversation_id']),
        ]

    def __str__(self):
        participant_names = [str(user) for user in self.participants.all()]
        return f"Conversation {self.conversation_id} - Participants: {', '.join(participant_names)}"
    
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['message_id']),
            models.Index(fields=['sender']),
            models.Index(fields='conversation'),
        ]
        ordering = ['sent_at']

    def __str__(self):
        return f"Message {self.message_id} from {self.sender} at {self.sent_at}"
