from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .ai_views import AIChatAPIView
from .views import ChatSessionViewSet, MessageViewSet

router = DefaultRouter()
router.register("sessions", ChatSessionViewSet, basename="chatsession")
router.register("messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", AIChatAPIView.as_view(), name="api-chat-ai"),
    path("", include(router.urls)),
]
