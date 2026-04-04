"""AI backends: OpenRouter (preferred), OpenAI, or Gemini. Config via environment."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Literal

from .resort_prompt import RESORT_ASSISTANT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

Provider = Literal["openrouter", "openai", "gemini"]


class AIConfigurationError(Exception):
    """Missing or invalid AI_* environment configuration."""

    pass


class AIUpstreamError(Exception):
    """The remote model API returned an error or unexpected payload."""

    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def _system_prompt() -> str:
    return os.environ.get("AI_SYSTEM_PROMPT") or RESORT_ASSISTANT_SYSTEM_PROMPT


def _openrouter_chat(user_message: str, timeout: int, *, system_content: str | None = None) -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise AIConfigurationError("OPENROUTER_API_KEY is not set.")

    model = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
    url = "https://openrouter.ai/api/v1/chat/completions"
    site_url = os.environ.get("SITE_URL", "http://127.0.0.1:8000")
    sys_msg = system_content if system_content is not None else _system_prompt()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.65,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": site_url,
            "X-Title": "Kuriftu Resort AI Concierge",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        logger.warning("OpenRouter HTTP error %s: %s", e.code, body[:500])
        raise AIUpstreamError("OpenRouter request failed.", status_code=e.code, body=body) from e
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            raise AIUpstreamError("OpenRouter request timed out.", status_code=504) from e
        logger.exception("OpenRouter network error")
        raise AIUpstreamError(f"Could not reach OpenRouter: {e}") from e
    except TimeoutError as e:
        raise AIUpstreamError("OpenRouter request timed out.", status_code=504) from e
    except OSError as e:
        logger.exception("OpenRouter network error")
        raise AIUpstreamError(f"Could not reach OpenRouter: {e}") from e

    try:
        out = json.loads(raw)
        return out["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logger.warning("Unexpected OpenRouter JSON: %s", raw[:800])
        raise AIUpstreamError("Unexpected response from OpenRouter.") from e


def _openai_chat(user_message: str, timeout: int, *, system_content: str | None = None) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise AIConfigurationError("OPENAI_API_KEY is not set.")

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    url = "https://api.openai.com/v1/chat/completions"
    sys_msg = system_content if system_content is not None else _system_prompt()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.65,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        logger.warning("OpenAI HTTP error %s: %s", e.code, body[:500])
        raise AIUpstreamError("OpenAI request failed.", status_code=e.code, body=body) from e
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            raise AIUpstreamError("OpenAI request timed out.", status_code=504) from e
        logger.exception("OpenAI network error")
        raise AIUpstreamError(f"Could not reach OpenAI: {e}") from e
    except TimeoutError as e:
        raise AIUpstreamError("OpenAI request timed out.", status_code=504) from e
    except OSError as e:
        logger.exception("OpenAI network error")
        raise AIUpstreamError(f"Could not reach OpenAI: {e}") from e

    try:
        out = json.loads(raw)
        return out["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logger.warning("Unexpected OpenAI JSON: %s", raw[:800])
        raise AIUpstreamError("Unexpected response from OpenAI.") from e


def _gemini_chat(user_message: str, timeout: int, *, system_content: str | None = None) -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise AIConfigurationError("GEMINI_API_KEY or GOOGLE_API_KEY is not set.")

    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        f"?key={urllib.parse.quote(key)}"
    )
    sys_msg = system_content if system_content is not None else _system_prompt()
    payload = {
        "systemInstruction": {"parts": [{"text": sys_msg}]},
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        logger.warning("Gemini HTTP error %s: %s", e.code, body[:500])
        raise AIUpstreamError("Gemini request failed.", status_code=e.code, body=body) from e
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            raise AIUpstreamError("Gemini request timed out.", status_code=504) from e
        logger.exception("Gemini network error")
        raise AIUpstreamError(f"Could not reach Gemini: {e}") from e
    except TimeoutError as e:
        raise AIUpstreamError("Gemini request timed out.", status_code=504) from e
    except OSError as e:
        logger.exception("Gemini network error")
        raise AIUpstreamError(f"Could not reach Gemini: {e}") from e

    try:
        out = json.loads(raw)
        cands = out.get("candidates") or []
        if not cands:
            raise AIUpstreamError("Gemini returned no candidates (safety filter or empty).", body=raw[:1000])
        parts = cands[0].get("content", {}).get("parts") or []
        return "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logger.warning("Unexpected Gemini JSON: %s", raw[:800])
        raise AIUpstreamError("Unexpected response from Gemini.") from e


def _choose_provider() -> Provider:
    """Explicit AI_PROVIDER wins; else first available key in openrouter → openai → gemini."""
    explicit = (os.environ.get("AI_PROVIDER") or "").strip().lower()
    if explicit == "openrouter":
        return "openrouter"
    if explicit == "openai":
        return "openai"
    if explicit == "gemini":
        return "gemini"
    if explicit and explicit != "auto":
        raise AIConfigurationError(
            f"AI_PROVIDER must be one of: openrouter, openai, gemini, auto (or unset). Got {explicit!r}."
        )
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    raise AIConfigurationError(
        "No AI key configured. Set OPENROUTER_API_KEY (recommended), or OPENAI_API_KEY, "
        "or GEMINI_API_KEY / GOOGLE_API_KEY. Optional: AI_PROVIDER=openrouter|openai|gemini."
    )


def get_ai_reply(user_message: str, *, timeout: int | None = None) -> tuple[str, Provider]:
    """
    Returns (reply_text, provider_name).
    """
    t = timeout if timeout is not None else int(os.environ.get("AI_REQUEST_TIMEOUT", "90"))
    provider = _choose_provider()
    if provider == "openrouter":
        return _openrouter_chat(user_message, t), "openrouter"
    if provider == "openai":
        return _openai_chat(user_message, t), "openai"
    return _gemini_chat(user_message, t), "gemini"


def get_ai_completion(
    user_message: str,
    *,
    system_prompt: str,
    timeout: int | None = None,
) -> tuple[str, Provider]:
    """
    Same transports as get_ai_reply but with a task-specific system prompt (e.g. JSON tools).
    """
    t = timeout if timeout is not None else int(os.environ.get("AI_REQUEST_TIMEOUT", "90"))
    provider = _choose_provider()
    if provider == "openrouter":
        return _openrouter_chat(user_message, t, system_content=system_prompt), "openrouter"
    if provider == "openai":
        return _openai_chat(user_message, t, system_content=system_prompt), "openai"
    return _gemini_chat(user_message, t, system_content=system_prompt), "gemini"
