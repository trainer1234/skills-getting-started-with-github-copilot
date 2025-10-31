import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities():
    """Deep-copy the in-memory activities before each test and restore after.
    This keeps tests isolated from mutations to the `activities` dict.
    """
    snapshot = copy.deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(snapshot)


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys from the app
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_remove_flow():
    client = TestClient(app)
    activity = "Chess Club"
    test_email = "testuser@example.com"

    # Ensure email not present initially
    resp = client.get("/activities")
    before = resp.json()
    assert test_email not in before[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Verify participant present
    resp = client.get("/activities")
    after = resp.json()
    assert test_email in after[activity]["participants"]

    # Remove participant
    resp = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 200
    body = resp.json()
    assert "Removed" in body.get("message", "")

    # Verify removed
    resp = client.get("/activities")
    final = resp.json()
    assert test_email not in final[activity]["participants"]
