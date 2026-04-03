from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    guest_count = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-check_in"]
        constraints = [
            models.CheckConstraint(
                check=Q(check_out__gt=F("check_in")),
                name="booking_check_out_after_check_in",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} — {self.room} ({self.check_in} → {self.check_out})"

    def clean(self):
        super().clean()
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")

    def overlapping_queryset(self):
        """Other bookings for the same room that overlap these dates (excluding self)."""
        qs = Booking.objects.filter(room_id=self.room_id).exclude(pk=self.pk or None)
        return qs.filter(
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        ).exclude(status=Booking.Status.CANCELLED)
