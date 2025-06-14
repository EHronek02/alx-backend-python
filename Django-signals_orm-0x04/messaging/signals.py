from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from datetime import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """Creates a notification for the receiver when a new message is sent"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )
        print(f"Created notification for {instance.receiver} about new message from {instance.sender}")


@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    """Track message edits and save previous content to history"""
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # save to message history
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                # update edit tracking fields
                instance.is_edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """clean up all related data when a user is deleted"""
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message hostry where user edited messages
    MessageHistory.objects.filter(edited_by=instance).delete()
