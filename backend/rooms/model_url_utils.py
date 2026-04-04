"""Classify virtual-twin model URLs for Sketchfab vs GLB/GLTF (<model-viewer>)."""

from __future__ import annotations

import re
from enum import Enum
from urllib.parse import urlparse


class ModelRenderKind(str, Enum):
    EMPTY = "empty"
    SKETCHFAB = "sketchfab"
    MODEL_VIEWER = "model_viewer"
    UNSUPPORTED = "unsupported"


def is_valid_http_url(s: str) -> bool:
    s = (s or "").strip()
    if not s or len(s) > 2000:
        return False
    try:
        p = urlparse(s)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except ValueError:
        return False


def classify_model_url(url: str) -> ModelRenderKind:
    """Pick renderer from stored URL (after resolve/fallback)."""
    if not (url or "").strip():
        return ModelRenderKind.EMPTY
    u = url.strip()
    if not is_valid_http_url(u):
        return ModelRenderKind.UNSUPPORTED
    low = u.lower()
    if "sketchfab.com" in low:
        return ModelRenderKind.SKETCHFAB
    path = low.split("?", 1)[0]
    if path.endswith(".glb") or path.endswith(".gltf"):
        return ModelRenderKind.MODEL_VIEWER
    return ModelRenderKind.UNSUPPORTED


def sketchfab_iframe_src(url: str) -> str:
    """
    Prefer …/models/<id>/embed for iframe (Sketchfab embed player).
    """
    u = (url or "").strip()
    if not u:
        return u
    low = u.lower()
    if "sketchfab.com" not in low:
        return u
    if "/embed" in low:
        return u
    m = re.search(r"sketchfab\.com/models/([a-f0-9]{32})", low)
    if m:
        return f"https://sketchfab.com/models/{m.group(1)}/embed"
    m2 = re.search(r"sketchfab\.com/3d-models/[\w-]+-([a-f0-9]{32})", low)
    if m2:
        return f"https://sketchfab.com/models/{m2.group(1)}/embed"
    return u
