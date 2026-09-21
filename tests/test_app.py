from uuid import UUID

from app.app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["service"] == "cloud-threat-modeling-demo"


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_generate_uuid():
    client = app.test_client()
    response = client.get("/uuid")
    assert response.status_code == 200
    assert response.is_json
    value = response.json["uuid"]
    parsed = UUID(value)
    assert parsed.version == 4
    assert str(parsed) == value


def test_generate_uuid_returns_fresh_values():
    client = app.test_client()
    first = client.get("/uuid")
    second = client.get("/uuid")
    assert first.json["uuid"] != second.json["uuid"]
