import asyncio
import json
from pathlib import Path

from asgi import app
from main import app as main_app


async def _call_app(method: str, path: str, body: bytes = b""):
    sent = []
    received_once = False

    async def receive():
        nonlocal received_once
        if not received_once:
            received_once = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "path": path,
        "headers": [],
    }

    await app(scope, receive, send)

    start = next(msg for msg in sent if msg["type"] == "http.response.start")
    body_msg = next(msg for msg in sent if msg["type"] == "http.response.body")
    return start, body_msg


def test_main_exports_same_asgi_app():
    assert main_app is app


def test_main_file_does_not_import_app_main_package():
    source = Path("main.py").read_text(encoding="utf-8")
    assert "from app.main import app" not in source


def test_asgi_get_serves_frontend():
    start, body = asyncio.run(_call_app("GET", "/"))

    assert start["status"] == 200
    assert b"Facebook Fanpage Traffic Analyzer" in body["body"]


def test_asgi_post_analyze_returns_summary():
    payload = {
        "followers": 10000,
        "avg_post_reach": 2500,
        "engagement_rate": 4.2,
        "posting_frequency_weekly": 4,
        "video_share_percent": 40,
        "response_time_minutes": 120,
        "ad_spend_usd_monthly": 500,
        "share_rate": 3.0,
    }
    start, body = asyncio.run(_call_app("POST", "/analyze", json.dumps(payload).encode("utf-8")))

    parsed = json.loads(body["body"].decode("utf-8"))
    assert start["status"] == 200
    assert "overall_score" in parsed
    assert len(parsed["top_drivers"]) == 3
