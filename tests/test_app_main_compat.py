import asyncio

from app.main import app


async def _call_get_root():
    sent = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "headers": [],
    }

    await app(scope, receive, send)
    return sent


def test_app_main_compat_serves_frontend():
    sent = asyncio.run(_call_get_root())
    start = next(msg for msg in sent if msg["type"] == "http.response.start")
    body = next(msg for msg in sent if msg["type"] == "http.response.body")

    assert start["status"] == 200
    assert b"Facebook Fanpage Traffic Analyzer" in body["body"]
