from django.contrib import admin

from .models import Room, RoomVirtualTwin


class RoomVirtualTwinInline(admin.StackedInline):
    model = RoomVirtualTwin
    max_num = 1
    can_delete = True
    fields = ("model_url", "audio_url", "climate_data")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "name", "room_type", "capacity", "price_per_night", "is_active")
    list_filter = ("room_type", "is_active")
    search_fields = ("name", "room_number", "description")
    inlines = [RoomVirtualTwinInline]


@admin.register(RoomVirtualTwin)
class RoomVirtualTwinAdmin(admin.ModelAdmin):
    list_display = ("room", "model_url_short", "updated_at")
    search_fields = ("room__name", "room__room_number", "model_url", "audio_url")
    fields = ("room", "model_url", "audio_url", "climate_data", "updated_at")
    readonly_fields = ("updated_at",)

    @admin.display(description="Model URL")
    def model_url_short(self, obj: RoomVirtualTwin) -> str:
        u = (obj.model_url or "").strip()
        return (u[:48] + "…") if len(u) > 48 else (u or "—")
