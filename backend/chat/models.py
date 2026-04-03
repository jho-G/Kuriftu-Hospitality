from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chat_sessions",
    )
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return self.title or f"Session #{self.pk}"


class Message(models.Model):
    class SenderRole(models.TextChoices):
        USER = "user", "Guest"
        STAFF = "staff", "Staff"
        SYSTEM = "system", "System"

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chat_messages",
    )
    sender_role = models.CharField(
        max_length=10,
        choices=SenderRole.choices,
        default=SenderRole.USER,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        preview = (self.content[:50] + "…") if len(self.content) > 50 else self.content
        return f"{self.sender_role}: {preview}"
