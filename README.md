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

### Option 2: uvicorn / ASGI

Preferred (avoids any potential local package naming conflicts):

```bash
python -m uvicorn asgi:app --reload
```

Compatibility alias (also works in this repo):

```bash
python -m uvicorn main:app --reload
```

Then open `http://localhost:8000`.

## Test

```bash
python -m pytest
```


## Troubleshooting

If you previously had `from app.main import app` in `main.py`, replace it with the current repo version.
That old import pattern can accidentally load an unrelated local `app` package and fail with missing dependencies such as `pdfplumber`.
