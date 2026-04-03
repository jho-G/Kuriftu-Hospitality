from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatSession, Message
from .serializers import (
    ChatSessionCreateSerializer,
    ChatSessionSerializer,
    MessageCreateSerializer,
    MessageSerializer,
)


class ChatSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ChatSession.objects.select_related("user", "booking").prefetch_related("messages")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ChatSessionCreateSerializer
        return ChatSessionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get", "post"], url_path="messages")
    def messages(self, request, pk=None):
        session = self.get_object()

        if request.method == "GET":
            msgs = session.messages.select_related("sender").order_by("created_at")
            return Response(MessageSerializer(msgs, many=True).data)

        ser = MessageCreateSerializer(
            data=request.data,
            context={"request": request, "session": session},
        )
        ser.is_valid(raise_exception=True)
        message = ser.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """Optional flat list of messages (filtered by session query param)."""

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Message.objects.select_related("session", "sender")
        session_id = self.request.query_params.get("session")
        if session_id:
            qs = qs.filter(session_id=session_id)
        if not self.request.user.is_staff:
            qs = qs.filter(session__user=self.request.user)
        return qs.order_by("-created_at")
