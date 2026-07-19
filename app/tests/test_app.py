from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
import main

client = TestClient(main.app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_mode"] in {"stub", "real"}


def test_modelcard():
    response = client.get("/modelcard")
    assert response.status_code == 200
    payload = response.json()
    assert payload["model"].startswith("multi-task")
    assert "disclaimer" in payload


def test_root_serves_frontend_html():
    response = client.get("/")
    assert response.status_code == 200
    text = response.text
    assert "Knee OA" in text
    assert "Assess (show everything)" in text
