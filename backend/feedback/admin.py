from django.contrib import admin

from .models import GuestFeedback


@admin.register(GuestFeedback)
class GuestFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "rating", "created_at")
    list_filter = ("category", "rating")
