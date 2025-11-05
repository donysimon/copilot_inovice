from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    """Test that the root endpoint redirects to the static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Test structure of response
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    
    # Test structure of an activity
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success(client: TestClient):
    """Test successful activity signup"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify the response message
    result = response.json()
    assert "message" in result
    assert result["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_already_registered(client: TestClient):
    """Test signup when student is already registered"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # This email is already registered in the test data
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    
    error = response.json()
    assert "detail" in error
    assert error["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity(client: TestClient):
    """Test signup for an activity that doesn't exist"""
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    
    error = response.json()
    assert "detail" in error
    assert error["detail"] == "Activity not found"