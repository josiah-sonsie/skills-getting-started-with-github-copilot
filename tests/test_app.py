from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    # Arrange: (No setup needed for root endpoint)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code in (200, 307, 308)
    assert "/static/index.html" in str(response.url)

def test_get_activities():
    # Arrange: (No setup needed for getting activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Act: Sign up
    resp_signup = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert: Signup
    assert resp_signup.status_code == 200
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]

    # Act: Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert: Unregister
    assert resp_unreg.status_code == 200
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]
