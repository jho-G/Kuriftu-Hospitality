from django.db import models


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
