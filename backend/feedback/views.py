from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import GuestFeedback
from .serializers import GuestFeedbackSerializer


class GuestFeedbackCreateView(generics.CreateAPIView):
    """
    POST JSON: {"category": "overall", "rating": 5, "comment": "..."}
    Same-origin browser requests must send the CSRF cookie + X-CSRFToken header.
    """

    queryset = GuestFeedback.objects.all()
    serializer_class = GuestFeedbackSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "success": True,
                "message": "Thank you - your feedback was saved.",
                "id": serializer.instance.pk,
            },
            status=201,
        )
