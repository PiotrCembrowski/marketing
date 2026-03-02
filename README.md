# Facebook Fanpage Traffic Analyzer

A simple frontend page plus Python backend API to explain why a Facebook fanpage gets traffic.

## What it does

- Provides a plain `index.html` front page (no React dependency).
- Sends metrics to `POST /analyze` and renders top drivers + weak areas.
- Falls back to a local frontend estimate if the backend is unavailable.
- Serves the same front page for any GET route (including `/analyze`) so users do not see `not found` text while navigating.

## Run

### Option 1: built-in HTTP server

```bash
python app.py
```

### Option 2: uvicorn / ASGI (recommended)

```bash
python -m uvicorn main:app --reload --port 8017
```

`main.py` now contains the ASGI app directly, so `uvicorn main:app` does not depend on an extra module import hop.

### Option 3: direct launcher

```bash
python run_server.py
```

Then open `http://localhost:8017`.

## Test

```bash
python -m pytest
```


## Troubleshooting

If you previously had `from app.main import app` in `main.py`, replace it with the current repo version.
That old import pattern can accidentally load an unrelated local `app` package and fail with missing dependencies such as `pdfplumber`.


### If you still get `from app.main import app` or `ImportError` from `main:app`

That traceback means your local `main.py` is not the one from this repo (or Python is importing another project path first).

Run these checks from the project root:

```bash
python -c "import main; print(main.__file__)"
python -c "import inspect, main; print(inspect.getsource(main))"
```

Expected result:
- `main.__file__` points to `<your-project>/main.py`
- source in `main.py` should include: `async def app(`

If it is not, fix local files and clear caches:

```bash
find . -name '__pycache__' -type d -prune -exec rm -rf {} +
python -m uvicorn main:app --reload --port 8017
```

Also make sure you run uvicorn **inside this repo directory** and with the same virtualenv where dependencies are installed.


### Why this fixes your specific traceback

Your traceback shows Python loading `from app.main import app`, which points into a different local `app/` package that imports `pdfplumber`.
This repo defines the ASGI app directly in `main.py`, reducing the chance of resolving a wrong external module during `uvicorn main:app`.


### Internal note

This repo now includes both `app.py` (runner script) and an `app/` compatibility package for `app.main:app`.
To avoid import collisions, the HTTP handler class lives in `http_server.py`.
