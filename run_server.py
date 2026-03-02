from __future__ import annotations

from fanpage_server import app


if __name__ == "__main__":
    import uvicorn

    # Using an app object directly avoids import-string resolution issues
    # from accidentally targeting the wrong module.
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
