from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number'
        ]
        read_only_fields = ['user_id']



class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='participants'
    )
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'conversation_id',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='sender'
    )
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        write_only=True,
        source='conversation'
    )

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'conversation_id', 'sender', 'sender_id', 'message_body', 'sent_at', 'read']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)