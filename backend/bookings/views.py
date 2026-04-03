from rest_framework import permissions, viewsets

from .models import Booking
from .serializers import BookingAdminSerializer, BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Booking.objects.select_related("user", "room")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action in ("update", "partial_update"):
            return BookingAdminSerializer
        return BookingSerializer
