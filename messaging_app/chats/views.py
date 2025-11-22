from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer,
    UserSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """
        Optionally filter conversations by participant
        """
        queryset = Conversation.objects.all()
        participant_id = self.request.query_params.get('participant', None)
        
        if participant_id is not None:
            queryset = queryset.filter(participants__user_id=participant_id)
        
        return queryset.distinct()
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        """
        Optionally filter messages by conversation
        """
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation', None)
        
        if conversation_id is not None:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure the sender is set to the current user (you might want to implement authentication)
        # For now, we'll use the sender from the request data
        message = serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
