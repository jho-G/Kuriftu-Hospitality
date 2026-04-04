"""AI-managed virtual room expectation (live report + client viewer payload)."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

from chat.ai_service import (
    AIConfigurationError,
    AIUpstreamError,
    get_ai_completion,
)

from .model_url_utils import ModelRenderKind, classify_model_url, is_valid_http_url as _is_valid_http_url

logger = logging.getLogger(__name__)

EXPECTATION_SYSTEM_PROMPT = """You are a luxury resort AI that configures a guest's *virtual room expectation* before arrival.

You MUST respond with a single JSON object only (no markdown fences, no commentary). Use this exact shape and types:

{
  "live_expectation_report": "<one or two sentences, first person, warm tone>",
  "commitment_guarantee": "<short promise that the physical room will match this virtual preview on arrival>",
  "scene": {
    "mood_label": "<Night|Dawn|Day|Sunset|Overcast — pick one that matches the story>",
    "ambient_intensity": <number 0.2-1.5>,
    "directional_color_hex": "<#RRGGBB warm/cool to match mood, e.g. golden-orange for Sunset>",
    "directional_intensity": <number 0.3-1.8>,
    "hemisphere_sky_hex": "<#RRGGBB upper 'window sky' tint>",
    "hemisphere_ground_hex": "<#RRGGBB lower bounce / floor tint>",
    "scene_background_hex": "<#RRGGBB full canvas background>",
    "window_tone": "<short phrase e.g. sunny afternoon, sunset glow>"
  },
  "comfort": {
    "target_temperature_c": <integer 18-24 suggested AC preview>,
    "ac_preview_active": <true|false>
  },
  "audio": {
    "should_autoplay": <true|false>,
    "volume": <number 0.0-1.0>
  }
}

Rules:
- Tie lighting to weather and time-of-day language (e.g. sunny 26°C → bright daylight; sunset → golden directional light).
- Mention location and temperature naturally inside live_expectation_report.
- commitment_guarantee must sound confident but professional.
"""


def _strip_code_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
        t = re.sub(r"\s*```\s*$", "", t)
    return t.strip()


def _safe_float(x: Any, default: float) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _safe_int(x: Any, default: int) -> int:
    try:
        return int(round(float(x)))
    except (TypeError, ValueError):
        return default


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _default_scene_for_weather(weather: dict[str, Any]) -> dict[str, Any]:
    cond = str(weather.get("condition", "clear")).lower()
    temp = _safe_float(weather.get("temp_c"), 24)
    if "sunset" in cond or "dusk" in cond:
        mood = "Sunset"
        return {
            "mood_label": mood,
            "ambient_intensity": 0.55,
            "directional_color_hex": "#ff8c42",
            "directional_intensity": 1.15,
            "hemisphere_sky_hex": "#ff6633",
            "hemisphere_ground_hex": "#1a0a05",
            "scene_background_hex": "#2a1510",
            "window_tone": "sunset glow",
        }
    if "rain" in cond or "storm" in cond or "overcast" in cond or "cloud" in cond:
        return {
            "mood_label": "Overcast",
            "ambient_intensity": 0.48,
            "directional_color_hex": "#c8d4e6",
            "directional_intensity": 0.75,
            "hemisphere_sky_hex": "#94a3b8",
            "hemisphere_ground_hex": "#1e293b",
            "scene_background_hex": "#1e293b",
            "window_tone": "soft overcast daylight",
        }
    if temp >= 28:
        amb = 1.35
        tone = "bright midday"
    elif temp >= 22:
        amb = 1.05
        tone = "warm afternoon"
    else:
        amb = 0.72
        tone = "cool daylight"
    return {
        "mood_label": "Day",
        "ambient_intensity": _clamp(amb, 0.2, 1.5),
        "directional_color_hex": "#fff5e0",
        "directional_intensity": 1.2,
        "hemisphere_sky_hex": "#87ceeb",
        "hemisphere_ground_hex": "#3d5c3d",
        "scene_background_hex": "#0f172a",
        "window_tone": tone,
    }


def _fallback_payload(
    room_status: dict[str, Any],
    current_weather: dict[str, Any],
    guest_profile: dict[str, Any],
) -> dict[str, Any]:
    loc = current_weather.get("location") or "the resort"
    temp = _safe_float(current_weather.get("temp_c"), 24)
    cond = current_weather.get("condition") or "pleasant"
    guest = guest_profile.get("name") or "Guest"
    scene = _default_scene_for_weather(current_weather)
    ac_on = temp > 24
    target_c = 21 if ac_on else _safe_int(temp, 22)
    report = (
        f"Since it is {cond} and about {temp:.0f}C in {loc}, I have preset your virtual view to match "
        f"{scene['window_tone']} lighting and tuned the comfort preview for your arrival, {guest}."
    )
    guarantee = (
        "I guarantee the physical room will match this 3D layout and comfort targets when you check in, "
        "subject to safety and same-day operations."
    )
    return {
        "live_expectation_report": report,
        "commitment_guarantee": guarantee,
        "scene": scene,
        "comfort": {
            "target_temperature_c": target_c,
            "ac_preview_active": ac_on,
        },
        "audio": {"should_autoplay": False, "volume": 0.65},
        "ai_provider": None,
        "ai_error": None,
        "ai_available": False,
    }


def _merge_ai_dict(parsed: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    out = dict(fallback)
    if not isinstance(parsed, dict):
        return out

    if isinstance(parsed.get("live_expectation_report"), str):
        out["live_expectation_report"] = parsed["live_expectation_report"].strip()
    if isinstance(parsed.get("commitment_guarantee"), str):
        out["commitment_guarantee"] = parsed["commitment_guarantee"].strip()

    fb_scene = dict(fallback.get("scene") or {})
    sc = parsed.get("scene")
    if isinstance(sc, dict):
        for k in (
            "mood_label",
            "ambient_intensity",
            "directional_color_hex",
            "directional_intensity",
            "hemisphere_sky_hex",
            "hemisphere_ground_hex",
            "scene_background_hex",
            "window_tone",
        ):
            if k in sc and sc[k] is not None:
                fb_scene[k] = sc[k]
        if "ambient_intensity" in fb_scene:
            fb_scene["ambient_intensity"] = _clamp(_safe_float(fb_scene["ambient_intensity"], 0.5), 0.2, 1.5)
        if "directional_intensity" in fb_scene:
            fb_scene["directional_intensity"] = _clamp(
                _safe_float(fb_scene["directional_intensity"], 1.0), 0.2, 2.0
            )
    out["scene"] = fb_scene

    fb_comfort = dict(fallback.get("comfort") or {})
    c = parsed.get("comfort")
    if isinstance(c, dict):
        if "target_temperature_c" in c:
            fb_comfort["target_temperature_c"] = int(
                _clamp(_safe_float(c["target_temperature_c"], 21), 16, 30)
            )
        if "ac_preview_active" in c:
            fb_comfort["ac_preview_active"] = bool(c["ac_preview_active"])
    out["comfort"] = fb_comfort

    fb_audio = dict(fallback.get("audio") or {})
    a = parsed.get("audio")
    if isinstance(a, dict):
        if "should_autoplay" in a:
            fb_audio["should_autoplay"] = bool(a["should_autoplay"])
        if "volume" in a:
            fb_audio["volume"] = _clamp(_safe_float(a["volume"], 0.65), 0.0, 1.0)
    out["audio"] = fb_audio

    return out


def get_room_expectation_summary(
    *,
    room_status: dict[str, Any],
    current_weather: dict[str, Any],
    guest_profile: dict[str, Any],
) -> dict[str, Any]:
    """
    Returns a dict suitable for JSON serialization to the virtual-room template:
    narrative fields, scene/lighting numbers, comfort + audio hints.
    """
    fallback = _fallback_payload(room_status, current_weather, guest_profile)
    user_payload = {
        "room_status": room_status,
        "current_weather": current_weather,
        "guest_profile": guest_profile,
    }
    user_message = (
        "Using the following JSON context, produce the response JSON as specified.\n\n"
        + json.dumps(user_payload, ensure_ascii=False, indent=2)
    )

    try:
        raw, provider = get_ai_completion(user_message, system_prompt=EXPECTATION_SYSTEM_PROMPT)
        cleaned = _strip_code_fence(raw)
        parsed = json.loads(cleaned)
        merged = _merge_ai_dict(parsed, fallback)
        merged["ai_available"] = True
        merged["ai_provider"] = provider
        merged["ai_error"] = None
        return merged
    except (AIConfigurationError, AIUpstreamError) as e:
        logger.info("Virtual expectation AI unavailable: %s", e)
        fallback["ai_error"] = str(e)
        return fallback
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.warning("Virtual expectation AI JSON parse failed: %s", e)
        fallback["ai_error"] = "Could not parse AI response."
        return fallback


def weather_context_from_request(request) -> dict[str, Any]:
    """Merge env defaults with optional query overrides for demos."""
    raw = os.environ.get("VIRTUAL_ROOM_WEATHER_JSON", "").strip()
    base: dict[str, Any] = {
        "location": "Bahir Dar, Ethiopia",
        "condition": "sunny",
        "temp_c": 26,
    }
    if raw:
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, dict):
                base.update({k: v for k, v in loaded.items() if v is not None})
        except json.JSONDecodeError:
            logger.warning("Invalid VIRTUAL_ROOM_WEATHER_JSON; using defaults.")

    q = request.GET
    if q.get("w_location"):
        base["location"] = q["w_location"]
    if q.get("w_condition"):
        base["condition"] = q["w_condition"]
    if q.get("w_temp"):
        try:
            base["temp_c"] = float(q["w_temp"])
        except ValueError:
            pass
    return base


def guest_profile_from_request(request) -> dict[str, Any]:
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        name = user.get_full_name() or getattr(user, "username", "") or "Guest"
        return {
            "name": name,
            "tier": getattr(user, "tier", "member") if hasattr(user, "tier") else "member",
            "is_authenticated": True,
        }
    return {"name": "Guest", "tier": "explorer", "is_authenticated": False}


def _configured_fallback_model_url() -> str:
    from django.conf import settings

    raw = (getattr(settings, "VIRTUAL_ROOM_FALLBACK_MODEL_URL", None) or "").strip()
    if not raw or not _is_valid_http_url(raw):
        return ""
    if classify_model_url(raw) not in (ModelRenderKind.SKETCHFAB, ModelRenderKind.MODEL_VIEWER):
        return ""
    return raw


def resolve_virtual_twin_client_assets(twin: Any) -> dict[str, Any]:
    """
    Resolve 3D viewer URL from RoomVirtualTwin.model_url (Sketchfab page/embed or .glb/.gltf).

    Optional site-wide fallback: settings.VIRTUAL_ROOM_FALLBACK_MODEL_URL (env), never hardcoded.
    """
    fallback = _configured_fallback_model_url()
    meta: dict[str, Any] = {
        "model_source": "none",
        "invalid_custom_url": False,
        "missing_database_url": False,
        "unsupported_format": False,
    }
    if not twin:
        return {
            "modelUrl": None,
            "audioUrl": None,
            "modelMeta": meta,
            "fallbackModelUrl": fallback or None,
        }

    raw_model = (getattr(twin, "model_url", None) or "").strip()
    if raw_model and _is_valid_http_url(raw_model):
        kind = classify_model_url(raw_model)
        if kind in (ModelRenderKind.SKETCHFAB, ModelRenderKind.MODEL_VIEWER):
            meta["model_source"] = "twin"
            model_url = raw_model
        else:
            meta["unsupported_format"] = True
            if fallback:
                meta["model_source"] = "fallback"
                model_url = fallback
            else:
                model_url = None
    elif raw_model:
        meta["invalid_custom_url"] = True
        if fallback:
            meta["model_source"] = "fallback"
            model_url = fallback
        else:
            model_url = None
    else:
        meta["missing_database_url"] = True
        if fallback:
            meta["model_source"] = "fallback"
            model_url = fallback
        else:
            model_url = None

    audio_raw = (getattr(twin, "audio_url", None) or "").strip()
    audio_url = audio_raw if audio_raw and _is_valid_http_url(audio_raw) else None

    return {
        "modelUrl": model_url,
        "audioUrl": audio_url,
        "modelMeta": meta,
        "fallbackModelUrl": fallback or None,
    }


def build_client_expectation_config(
    *,
    expectation: dict[str, Any],
    twin,
    room_id: int | None = None,
) -> dict[str, Any]:
    """Payload for `json_script` + client UI (audio, expectation); model URL drives server-side viewer choice."""
    assets = resolve_virtual_twin_client_assets(twin)
    return {
        "modelUrl": assets["modelUrl"],
        "audioUrl": assets["audioUrl"],
        "modelMeta": assets["modelMeta"],
        "fallbackModelUrl": assets["fallbackModelUrl"],
        "roomId": room_id,
        "expectation": expectation,
    }
