from rest_framework import permissions
from .models import Conversation, Message

class IsParticipant(permissions.BasePermission):
    """Custom permission to only allow participants of a conversation
    to access it"""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
    
class IsMessageSenderOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or request.user in obj.conversation.participants.all()


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Allow access only to authenticated users who are participants
      of the conversation.
    - Works for Conversation and Message objects.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If the object is a Conversation, check participation
        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()

        # If the object is a Message, check participation in the conversation
        if isinstance(obj, Message):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False
