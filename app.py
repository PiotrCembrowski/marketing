from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from analyzer import FanpageMetrics, analyze_traffic_drivers, summarize_analysis

TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"
ANALYZE_ROUTE = "/analyze"


class AnalyzerHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_frontend(self) -> None:
        if not TEMPLATE_PATH.exists():
            self._send_json({"error": "Front page template not found."}, status=500)
            return

        html = TEMPLATE_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def do_GET(self) -> None:  # noqa: N802
        # Always serve the frontend for browser navigation routes,
        # including /analyze, to avoid confusing "Not Found" pages.
        self._serve_frontend()

    def do_POST(self) -> None:  # noqa: N802
        route = urlsplit(self.path).path
        if route != ANALYZE_ROUTE:
            self._send_json({"error": "Not found"}, status=404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8"))

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
            self._send_json({"error": "Invalid input values. Please provide numeric fields."}, status=400)
            return

        drivers = analyze_traffic_drivers(metrics)
        summary = summarize_analysis(drivers)
        self._send_json(summary)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AnalyzerHandler)
    print("Running on http://0.0.0.0:8000")
    server.serve_forever()
