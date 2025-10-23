import pytest

pytest.importorskip("ag_ui_adk")

from fastapi.testclient import TestClient  # noqa: E402

from aido.api import app  # noqa: E402


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sessions_endpoint_returns_list():
    response = client.get("/api/sessions")
    assert response.status_code == 200
    body = response.json()
    assert "sessions" in body
    assert isinstance(body["sessions"], list)
