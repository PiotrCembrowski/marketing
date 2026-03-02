import http.client
import json
import threading
from http.server import HTTPServer

from app import AnalyzerHandler


FRONTEND_TITLE = "Facebook Fanpage Traffic Analyzer"


def _start_server():
    server = HTTPServer(("127.0.0.1", 0), AnalyzerHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_front_page_routes_are_available():
    server, thread = _start_server()
    conn = http.client.HTTPConnection("127.0.0.1", server.server_port)

    try:
        for route in ["/", "/index.html", "/frontpage", "/anything"]:
            conn.request("GET", route)
            response = conn.getresponse()
            body = response.read().decode("utf-8")
            assert response.status == 200
            assert FRONTEND_TITLE in body
    finally:
        conn.close()
        server.shutdown()
        thread.join(timeout=1)


def test_analyze_route_requires_post():
    server, thread = _start_server()
    conn = http.client.HTTPConnection("127.0.0.1", server.server_port)

    try:
        conn.request("GET", "/analyze")
        response = conn.getresponse()
        response.read()
        assert response.status == 405
    finally:
        conn.close()
        server.shutdown()
        thread.join(timeout=1)


def test_analyze_endpoint_returns_json_summary():
    server, thread = _start_server()
    conn = http.client.HTTPConnection("127.0.0.1", server.server_port)

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

    try:
        conn.request(
            "POST",
            "/analyze",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert "overall_score" in body
        assert len(body["top_drivers"]) == 3
    finally:
        conn.close()
        server.shutdown()
        thread.join(timeout=1)
