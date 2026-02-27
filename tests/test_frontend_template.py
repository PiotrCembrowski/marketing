from pathlib import Path


def test_template_contains_plain_frontend_elements():
    html = Path("templates/index.html").read_text(encoding="utf-8")

    assert "Facebook Fanpage Traffic Analyzer" in html
    assert "<form id=\"analyzer-form\">" in html
    assert "Analyze Traffic" in html
    assert "fetch('/analyze'" in html
