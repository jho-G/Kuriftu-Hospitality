"""Run: python scripts/verify_csrf.py (from backend/)"""
import os
import re
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client  # noqa: E402


def csrf_from(html: str) -> str:
    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    assert m, "no csrf token in page"
    return m.group(1)


def main() -> None:
    c = Client(enforce_csrf_checks=True)
    r = c.get("/feedback/")
    token = csrf_from(r.content.decode("utf-8"))
    out = c.post(
        "/api/feedback/",
        data={"category": "overall", "rating": 4, "comment": "csrf test"},
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token,
    )
    print("feedback csrf", out.status_code, out.json() if out.status_code == 201 else out.content[:200])

    r2 = c.get("/chat/")
    token2 = csrf_from(r2.content.decode("utf-8"))
    out2 = c.post(
        "/api/chat/",
        data={"message": "csrf hi"},
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token2,
    )
    print("chat csrf", out2.status_code, "ok" if out2.status_code == 200 else out2.content[:200])


if __name__ == "__main__":
    main()
