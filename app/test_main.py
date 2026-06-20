"""Basic tests so the CI pipeline has a real 'test' step to run."""
from app.main import app


def test_ping():
    client = app.test_client()
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.data == b"pong"


def test_healthz():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
