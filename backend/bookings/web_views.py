from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rooms.models import Room

from .forms import BookingForm
from .models import Booking


@login_required
def book_room(request, room_id: int):
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, room=room)
        if form.is_valid():
            booking = form.save()
            messages.success(request, "Your booking request was submitted.")
            return redirect("booking_confirmation", pk=booking.pk)
    else:
        form = BookingForm(user=request.user, room=room)
    return render(
        request,
        "bookings/book_room.html",
        {
            "form": form,
            "room": room,
            "nav_active": "rooms",
        },
    )


@login_required
def booking_confirmation(request, pk: int):
    booking = get_object_or_404(Booking.objects.select_related("room"), pk=pk)
    if booking.user_id != request.user.id and not request.user.is_staff:
        messages.error(request, "You do not have access to this booking.")
        return redirect("dashboard")
    return render(
        request,
        "bookings/booking_confirmation.html",
        {
            "booking": booking,
            "nav_active": "dashboard",
        },
    )
