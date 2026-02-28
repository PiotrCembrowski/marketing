from __future__ import annotations

import json
from pathlib import Path
from analyzer import FanpageMetrics, analyze_traffic_drivers, summarize_analysis

TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"
ANALYZE_ROUTE = "/analyze"


async def app(scope, receive, send):
    if scope["type"] != "http":
        await _send_json(send, {"error": "Unsupported scope type"}, status=500)
        return

    method = scope["method"].upper()
    path = scope.get("path", "/")

    if method == "GET":
        await _serve_frontend(send)
        return

    if method == "POST" and path == ANALYZE_ROUTE:
        await _handle_analyze(receive, send)
        return

    await _send_json(send, {"error": "Not found"}, status=404)


async def _serve_frontend(send):
    if not TEMPLATE_PATH.exists():
        await _send_json(send, {"error": "Front page template not found."}, status=500)
        return

    html = TEMPLATE_PATH.read_bytes()
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/html; charset=utf-8"),
                (b"content-length", str(len(html)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": html})


async def _handle_analyze(receive, send):
    body = b""
    while True:
        message = await receive()
        if message["type"] != "http.request":
            continue
        body += message.get("body", b"")
        if not message.get("more_body", False):
            break

    try:
        payload = json.loads(body.decode("utf-8") or "{}")
        metrics = FanpageMetrics(
            followers=int(payload.get("followers", 0)),
            avg_post_reach=int(payload.get("avg_post_reach", 0)),
            engagement_rate=float(payload.get("engagement_rate", 0)),
            posting_frequency_weekly=int(payload.get("posting_frequency_weekly", 0)),
            video_share_percent=float(payload.get("video_share_percent", 0)),
            response_time_minutes=int(payload.get("response_time_minutes", 0)),
            ad_spend_usd_monthly=float(payload.get("ad_spend_usd_monthly", 0)),
            share_rate=float(payload.get("share_rate", 0)),
        )
    except (ValueError, TypeError, json.JSONDecodeError):
        await _send_json(send, {"error": "Invalid input values. Please provide numeric fields."}, status=400)
        return

    summary = summarize_analysis(analyze_traffic_drivers(metrics))
    await _send_json(send, summary, status=200)


async def _send_json(send, payload: dict, status: int):
    body = json.dumps(payload).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})
