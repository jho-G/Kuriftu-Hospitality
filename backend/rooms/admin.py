from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "name", "room_type", "capacity", "price_per_night", "is_active")
    list_filter = ("room_type", "is_active")
    search_fields = ("name", "room_number", "description")
