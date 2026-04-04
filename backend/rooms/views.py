from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets

from .model_url_utils import ModelRenderKind, classify_model_url, sketchfab_iframe_src
from .models import Room, RoomVirtualTwin
from .serializers import RoomSerializer
from .services import (
    build_client_expectation_config,
    get_room_expectation_summary,
    guest_profile_from_request,
    weather_context_from_request,
)


def room_catalog(request):
    rooms = (
        Room.objects.filter(is_active=True)
        .order_by("room_number")
        .annotate(
            has_virtual_twin=Exists(
                RoomVirtualTwin.objects.filter(room_id=OuterRef("pk")),
            ),
        )
    )
    return render(
        request,
        "rooms/room_list.html",
        {"rooms": rooms, "nav_active": "rooms"},
    )


def room_detail(request, pk: int):
    room = get_object_or_404(
        Room.objects.annotate(
            has_virtual_twin=Exists(
                RoomVirtualTwin.objects.filter(room_id=OuterRef("pk")),
            ),
        ),
        pk=pk,
        is_active=True,
    )
    return render(
        request,
        "rooms/room_detail.html",
        {"room": room, "nav_active": "rooms"},
    )


def virtual_rooms_list(request):
    rooms = (
        Room.objects.filter(is_active=True)
        .order_by("room_number")
        .annotate(
            has_virtual_twin=Exists(
                RoomVirtualTwin.objects.filter(room_id=OuterRef("pk")),
            ),
        )
    )
    return render(
        request,
        "virtual_rooms_list.html",
        {
            "rooms": rooms,
            "nav_active": "virtual_rooms",
        },
    )


def _build_virtual_room_context(request, room: Room):
    try:
        twin = room.virtual_twin
    except RoomVirtualTwin.DoesNotExist:
        twin = None
    climate_data = twin.climate_data if twin else {}
    climate_items = [
        (str(k).replace("_", " ").strip().title(), v) for k, v in climate_data.items()
    ]
    room_status = {
        "id": room.id,
        "name": room.name,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "is_active": room.is_active,
        "capacity": room.capacity,
        "description": (room.description or "")[:400],
        "twin_climate": climate_data,
    }
    current_weather = weather_context_from_request(request)
    guest_profile = guest_profile_from_request(request)
    expectation = get_room_expectation_summary(
        room_status=room_status,
        current_weather=current_weather,
        guest_profile=guest_profile,
    )
    expectation_client_config = build_client_expectation_config(
        expectation=expectation,
        twin=twin,
        room_id=room.pk,
    )
    twin_model_meta = expectation_client_config["modelMeta"] if twin else None
    twin_audio_url = expectation_client_config.get("audioUrl") if twin else None
    resolved_model_url = (expectation_client_config.get("modelUrl") or "").strip()
    model_render_kind = classify_model_url(resolved_model_url)
    viewer_3d_available = model_render_kind in (
        ModelRenderKind.SKETCHFAB,
        ModelRenderKind.MODEL_VIEWER,
    )
    sketchfab_embed_src = (
        sketchfab_iframe_src(resolved_model_url)
        if model_render_kind == ModelRenderKind.SKETCHFAB
        else ""
    )
    model_viewer_src = (
        resolved_model_url
        if model_render_kind == ModelRenderKind.MODEL_VIEWER
        else ""
    )
    return {
        "room": room,
        "twin": twin,
        "climate_data": climate_data,
        "climate_items": climate_items,
        "expectation": expectation,
        "expectation_client_config": expectation_client_config,
        "twin_model_meta": twin_model_meta,
        "twin_audio_url": twin_audio_url,
        "viewer_3d_available": viewer_3d_available,
        "model_render_kind": model_render_kind.value,
        "sketchfab_embed_src": sketchfab_embed_src,
        "model_viewer_src": model_viewer_src,
        "nav_active": "virtual_rooms",
    }


def room_virtual_preview(request, room_id: int):
    room = get_object_or_404(
        Room.objects.select_related("virtual_twin"),
        pk=room_id,
        is_active=True,
    )
    ctx = _build_virtual_room_context(request, room)
    if request.user.is_authenticated:
        return render(request, "room_virtual_viewer.html", ctx)
    return render(request, "room_virtual_limited.html", ctx)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
