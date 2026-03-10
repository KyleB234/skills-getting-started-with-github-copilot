from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_expected_structure():
    # Arrange: nothing special to set up; app has known seed data

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant_and_prevents_duplicate():
    # Arrange
    activity = "Chess Club"
    new_student = "test@student.edu"

    # Act: first signup
    first = client.post(f"/activities/{activity}/signup", params={"email": new_student})

    # Assert first signup succeeds
    assert first.status_code == 200
    assert "Signed up" in first.json()["message"]

    # Act: duplicate signup
    second = client.post(f"/activities/{activity}/signup", params={"email": new_student})

    # Assert second signup fails with 400
    assert second.status_code == 400
    assert second.json()["detail"] == "Student already signed up for this activity"


def test_delete_removes_participant_and_returns_404_when_missing():
    # Arrange
    activity = "Programming Class"
    existing_student = "emma@mergington.edu"

    # Act: remove an existing student
    delete_resp = client.delete(f"/activities/{activity}/signup", params={"email": existing_student})

    # Assert remove succeeds
    assert delete_resp.status_code == 200
    assert "Unregistered" in delete_resp.json()["message"]

    # Act: remove again (should not exist)
    delete_again = client.delete(f"/activities/{activity}/signup", params={"email": existing_student})

    # Assert second removal returns 404
    assert delete_again.status_code == 404
    assert delete_again.json()["detail"] == "Student not registered for this activity"


def test_signup_and_delete_on_nonexistent_activity_return_404():
    # Arrange
    bad_activity = "Nonexistent Club"
    email = "nobody@mergington.edu"

    # Act: signup
    signup_resp = client.post(f"/activities/{bad_activity}/signup", params={"email": email})
    # Act: delete
    delete_resp = client.delete(f"/activities/{bad_activity}/signup", params={"email": email})

    # Assert
    assert signup_resp.status_code == 404
    assert signup_resp.json()["detail"] == "Activity not found"

    assert delete_resp.status_code == 404
    assert delete_resp.json()["detail"] == "Activity not found"
