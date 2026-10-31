from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    existing = client.get("/activities").json()
    if email in existing[activity_name]["participants"]:
        client.delete(f"/activities/{activity_name}/participants?email={email}")

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200

    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]
