from rest_framework import generics, permissions, viewsets

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Staff-only user directory; authenticated users may retrieve self via /me/."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(pk=self.request.user.pk)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
