from pathlib import Path

from fanpage_server import app
from run_server import app as run_server_app


def test_run_server_exports_same_app_object():
    assert run_server_app is app


def test_run_server_uses_direct_app_object_with_uvicorn():
    source = Path("run_server.py").read_text(encoding="utf-8")
    assert "uvicorn.run(app" in source
    assert "main:app" not in source
