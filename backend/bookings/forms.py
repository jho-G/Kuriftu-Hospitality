from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from rooms.models import Room

from .models import Booking

_BOOK_WIDGET_ATTRS = {
    "style": "width:100%;max-width:20rem;box-sizing:border-box;padding:0.6rem 0.75rem;border:1px solid rgba(45,38,32,0.22);border-radius:8px;font-size:1rem;",
}


class BookingForm(forms.ModelForm):
    """Authenticated web booking (parity with BookingSerializer validation)."""

    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guest_count", "notes")
        widgets = {
            "check_in": forms.DateInput(
                attrs={"type": "date", **_BOOK_WIDGET_ATTRS},
            ),
            "check_out": forms.DateInput(
                attrs={"type": "date", **_BOOK_WIDGET_ATTRS},
            ),
            "guest_count": forms.NumberInput(attrs=_BOOK_WIDGET_ATTRS),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "style": _BOOK_WIDGET_ATTRS["style"] + "max-width:100%;",
                },
            ),
        }

    def __init__(self, *args, user, room: Room, **kwargs):
        self.user = user
        self.room = room
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")
        if check_in and check_out and check_out <= check_in:
            raise ValidationError("Check-out must be after check-in.")
        if check_in and check_in < timezone.now().date():
            raise ValidationError({"check_in": "Cannot book dates in the past."})
        if check_in and check_out and self.room:
            conflict = (
                Booking.objects.filter(
                    room=self.room,
                    check_in__lt=check_out,
                    check_out__gt=check_in,
                )
                .exclude(status=Booking.Status.CANCELLED)
            )
            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                raise ValidationError(
                    "This room is already booked for overlapping dates.",
                )
        return cleaned

    def save(self, commit: bool = True) -> Booking:
        booking = super().save(commit=False)
        booking.user = self.user
        booking.room = self.room
        check_in = self.cleaned_data["check_in"]
        check_out = self.cleaned_data["check_out"]
        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValidationError("Invalid stay length.")
        booking.total_price = self.room.price_per_night * Decimal(nights)
        booking.status = Booking.Status.PENDING
        if commit:
            booking.save()
        return booking
