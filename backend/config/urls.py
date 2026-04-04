"""Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rooms.views import (
    room_catalog,
    room_detail,
    room_virtual_preview,
    virtual_rooms_list,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html", extra_context={"nav_active": "home"}), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html", extra_context={"nav_active": "about"}), name="about"),
    path("villas/", TemplateView.as_view(template_name="villas.html", extra_context={"nav_active": "villas"}), name="villas"),
    path("experiences/", TemplateView.as_view(template_name="experiences.html", extra_context={"nav_active": "experiences"}), name="experiences"),
    path("events/", TemplateView.as_view(template_name="events.html", extra_context={"nav_active": "events"}), name="events"),
    path("chat/", TemplateView.as_view(template_name="chat.html", extra_context={"nav_active": "chat"}), name="chat"),
    path("smart-room/", TemplateView.as_view(template_name="smart_room.html", extra_context={"nav_active": "smart_room"}), name="smart_room"),
    path("feedback/", TemplateView.as_view(template_name="feedback.html", extra_context={"nav_active": "feedback"}), name="feedback"),
    path("accounts/", include("users.urls_web")),
    path("", include("bookings.urls_web")),
    path("rooms/", room_catalog, name="room_list"),
    path("rooms/<int:pk>/", room_detail, name="room_detail"),
    path("virtual-rooms/", virtual_rooms_list, name="virtual_rooms"),
    path(
        "rooms/<int:room_id>/virtual/",
        room_virtual_preview,
        name="room_virtual_preview",
    ),
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/rooms/", include("rooms.urls")),
    path("api/bookings/", include("bookings.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/feedback/", include("feedback.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
