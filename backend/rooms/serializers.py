from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "room_number",
            "room_type",
            "capacity",
            "price_per_night",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
