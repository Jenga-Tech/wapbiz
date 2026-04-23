from fastapi.testclient import TestClient

from app.main import app


def test_onboarding_status() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/onboarding/status")

    assert response.status_code == 200
    body = response.json()
    assert "message" in body