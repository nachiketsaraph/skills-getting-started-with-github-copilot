import uuid
from urllib.parse import urlencode
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_duplicate_and_remove():
    email = f"test{uuid.uuid4().hex}@example.com"

    # Sign up
    resp = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities["Basketball"]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp_dup.status_code == 400

    # Remove participant
    resp_del = client.delete(f"/activities/Basketball/participants?email={email}")
    assert resp_del.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Basketball"]["participants"]

    # Removing again should return 404
    resp_del2 = client.delete(f"/activities/Basketball/participants?email={email}")
    assert resp_del2.status_code == 404
