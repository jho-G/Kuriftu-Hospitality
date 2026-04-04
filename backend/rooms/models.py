from django.db import models


class RoomVirtualTwin(models.Model):
    """3D / sensory preview assets for a room (virtual expectation experience)."""

    room = models.OneToOneField(
        "Room",
        on_delete=models.CASCADE,
        related_name="virtual_twin",
    )
    model_url = models.URLField(
        max_length=500,
        blank=True,
        help_text=(
            "HTTPS URL for this room’s 3D preview: a Sketchfab model or embed link (sketchfab.com), "
            "or a direct link to a .glb / .gltf file. "
            "If empty, VIRTUAL_ROOM_FALLBACK_MODEL_URL (environment) is used when set."
        ),
    )
    audio_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Optional HTTPS link to ambient audio (mp3, ogg, wav).",
    )
    climate_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='e.g. {"temperature_c": 22, "scent": "Jasmine"}',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "room virtual twin"
        verbose_name_plural = "room virtual twins"

    def __str__(self) -> str:
        return f"Virtual twin — {self.room}"


class Room(models.Model):
    name = models.CharField(max_length=120)
    room_number = models.CharField(max_length=32, unique=True, db_index=True)
    room_type = models.CharField(max_length=64)
    capacity = models.PositiveSmallIntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["room_number"]

    def __str__(self) -> str:
        return f"{self.room_number} — {self.name}"
