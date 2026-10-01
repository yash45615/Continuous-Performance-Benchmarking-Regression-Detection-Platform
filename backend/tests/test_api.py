from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_products():

    response = client.get(
        "/products/?limit=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )