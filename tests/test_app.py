"""Tests for the FastAPI extracurricular activities application."""

import pytest


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Drama Club" in data
    
    def test_get_activities_contains_required_fields(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, details in data.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
    
    def test_get_activities_participants_are_lists(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, details in data.items():
            assert isinstance(details["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant_success(self, client):
        """Test successfully signing up a new participant."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newemail@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newemail@mergington.edu" in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup adds the participant to the activity."""
        email = "newstudent@mergington.edu"
        
        # Signup
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant_fails(self, client):
        """Test that signing up the same participant twice fails."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signing up for a nonexistent activity fails."""
        response = client.post(
            "/activities/NonExistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_signup_multiple_participants(self, client):
        """Test signing up multiple different participants."""
        emails = ["test1@mergington.edu", "test2@mergington.edu", "test3@mergington.edu"]
        
        for email in emails:
            response = client.post(
                "/activities/Gym Class/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all were added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        for email in emails:
            assert email in activities["Gym Class"]["participants"]


class TestUnregisterEndpoint:
    """Tests for the POST /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_existing_participant_success(self, client):
        """Test successfully unregistering an existing participant."""
        email = "michael@mergington.edu"
        
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister removes the participant from the activity."""
        email = "daniel@mergington.edu"
        
        # Verify participant exists
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Chess Club"]["participants"]
        
        # Unregister
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_participant_fails(self, client):
        """Test that unregistering a non-participant fails."""
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        """Test that unregistering from a nonexistent activity fails."""
        response = client.post(
            "/activities/NonExistent Club/unregister",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_signup_then_unregister(self, client):
        """Test signing up and then unregistering a participant."""
        email = "tempstudent@mergington.edu"
        activity = "Debate Team"
        
        # Signup
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signup
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
        
        # Unregister
        unregister_response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify unregister
        activities = client.get("/activities").json()
        assert email not in activities[activity]["participants"]


class TestRootEndpoint:
    """Tests for the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]
