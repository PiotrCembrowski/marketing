<<<<<<< HEAD
# marketing
=======
# Facebook Fanpage Traffic Analyzer

A simple frontend page plus Python backend API to explain why a Facebook fanpage gets traffic.

## What it does

- Provides a plain `index.html` front page (no React dependency).
- Sends metrics to `POST /analyze` and renders top drivers + weak areas.
- Falls back to a local frontend estimate if the backend is unavailable.
- Serves the same front page for any GET route so users do not see `not found` by accident.

## Run

```bash
python app.py
```

Then open `http://localhost:8000`.

## Test

```bash
python -m pytest
```
>>>>>>> 592097c4704c5e5e058d70ed149ead9fc5bc5591
