from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


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

