from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        return self.queryset.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise permissions.PermissionDenied(
                "You are not a participant in this conversation"
            )
        serializer.save(sender=self.request.user)
