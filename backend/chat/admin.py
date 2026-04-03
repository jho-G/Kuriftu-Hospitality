from django.contrib import admin

from .models import ChatSession, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "booking", "title", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("title", "user__username")
    raw_id_fields = ("user", "booking")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "sender", "sender_role", "created_at")
    list_filter = ("sender_role",)
    search_fields = ("content",)
    raw_id_fields = ("session", "sender")
