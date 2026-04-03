from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from rooms.models import Room

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source="room.room_number", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "user",
            "room",
            "room_number",
            "check_in",
            "check_out",
            "status",
            "guest_count",
            "total_price",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "status", "total_price", "created_at", "updated_at")

    def validate(self, attrs):
        check_in = attrs.get("check_in") or (self.instance and self.instance.check_in)
        check_out = attrs.get("check_out") or (self.instance and self.instance.check_out)
        room = attrs.get("room") or (self.instance and self.instance.room)

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError("Check-out must be after check-in.")

        creating = self.instance is None
        if creating and check_in and check_in < timezone.now().date():
            raise serializers.ValidationError({"check_in": "Cannot book dates in the past."})

        if room and check_in and check_out:
            conflict = (
                Booking.objects.filter(room=room, check_in__lt=check_out, check_out__gt=check_in)
                .exclude(status=Booking.Status.CANCELLED)
            )
            if self.instance:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                raise serializers.ValidationError(
                    "This room is already booked for overlapping dates.",
                )

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        room: Room = validated_data["room"]
        check_in = validated_data["check_in"]
        check_out = validated_data["check_out"]
        nights = (check_out - check_in).days
        if nights <= 0:
            raise serializers.ValidationError("Invalid stay length.")
        validated_data["total_price"] = room.price_per_night * Decimal(nights)
        validated_data["status"] = Booking.Status.PENDING
        return super().create(validated_data)


class BookingAdminSerializer(BookingSerializer):
    """Staff can set status."""

    class Meta(BookingSerializer.Meta):
        read_only_fields = ("id", "user", "total_price", "created_at", "updated_at")
