from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    """Defines User serializer"""
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'message_body',
            'sent_at',
            'read']
        read_only_fields = ['message_id', 'sender', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        field = ['conversation_id', 'participants', 'created_at', 'updated_at', 'last_message']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

        def get_last_message(self, obj):
            last_message = obj.messages.last()
            if last_message:
                return MessageSerializer(last_message).data
            return None


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        model = Conversation
        fields = ['participants']
