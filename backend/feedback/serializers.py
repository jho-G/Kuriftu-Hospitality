from rest_framework import serializers

from .models import GuestFeedback


class GuestFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestFeedback
        fields = ("id", "category", "rating", "comment", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
