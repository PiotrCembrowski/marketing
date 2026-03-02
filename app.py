from __future__ import annotations

from http.server import HTTPServer

from http_server import AnalyzerHandler


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8017), AnalyzerHandler)
    print("Running on http://0.0.0.0:8017")
    server.serve_forever()
