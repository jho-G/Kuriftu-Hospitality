"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html", extra_context={"nav_active": "home"}), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html", extra_context={"nav_active": "about"}), name="about"),
    path("villas/", TemplateView.as_view(template_name="villas.html", extra_context={"nav_active": "villas"}), name="villas"),
    path("experiences/", TemplateView.as_view(template_name="experiences.html", extra_context={"nav_active": "experiences"}), name="experiences"),
    path("events/", TemplateView.as_view(template_name="events.html", extra_context={"nav_active": "events"}), name="events"),
    path("chat/", TemplateView.as_view(template_name="chat.html", extra_context={"nav_active": "chat"}), name="chat"),
    path("smart-room/", TemplateView.as_view(template_name="smart_room.html", extra_context={"nav_active": "smart_room"}), name="smart_room"),
    path("feedback/", TemplateView.as_view(template_name="feedback.html", extra_context={"nav_active": "feedback"}), name="feedback"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/rooms/", include("rooms.urls")),
    path("api/bookings/", include("bookings.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/feedback/", include("feedback.urls")),
]
