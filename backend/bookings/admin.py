from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "check_in", "check_out", "status", "guest_count")
    list_filter = ("status", "check_in")
    search_fields = ("user__username", "room__room_number", "notes")
    raw_id_fields = ("user", "room")
    date_hierarchy = "check_in"
