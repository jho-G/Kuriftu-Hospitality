from rest_framework import serializers

from .models import ChatSession, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "session",
            "sender",
            "sender_role",
            "content",
            "created_at",
        )
        read_only_fields = ("id", "sender", "created_at")


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = (
            "id",
            "user",
            "booking",
            "title",
            "messages",
            "message_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def get_message_count(self, obj):
        return obj.messages.count()


class ChatSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ("booking", "title")


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("content",)

    def create(self, validated_data):
        session: ChatSession = self.context["session"]
        request = self.context["request"]
        validated_data["session"] = session
        validated_data["sender"] = request.user
        validated_data["sender_role"] = (
            Message.SenderRole.STAFF if request.user.is_staff else Message.SenderRole.USER
        )
        return super().create(validated_data)


class AIChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=16000, trim_whitespace=True)
