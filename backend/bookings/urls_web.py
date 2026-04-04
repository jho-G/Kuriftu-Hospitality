from django.urls import path

from .web_views import book_room, booking_confirmation

urlpatterns = [
    path("rooms/<int:room_id>/book/", book_room, name="book_room"),
    path("bookings/<int:pk>/confirmation/", booking_confirmation, name="booking_confirmation"),
]
