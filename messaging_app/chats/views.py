from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer
)
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing conversations.
    """
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        """
        Return only conversations where the current user is a participant
        """
        return self.queryset.filter(participants=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Retrieve all messages for a specific conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure the current user is included in participants
        participants = serializer.validated_data.get('participants', [])
        if request.user not in participants:
            participants.append(request.user)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only messages in conversations where the current user is a participant
        """
        return self.queryset.filter(
            conversation__participants=self.request.user
        ).order_by('-sent_at')

    def perform_create(self, serializer):
        """
        Automatically set the sender to the current user
        and verify they're a conversation participant
        """
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise permissions.PermissionDenied(
                "You are not a participant in this conversation"
            )
        serializer.save(sender=self.request.user)
