"""Pytest configuration and fixtures for FastAPI app tests."""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities before each test to ensure test isolation."""
    from app import activities
    
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Explore acting, theater production, and perform in school plays",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["sarah@mergington.edu", "james@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills through competitive debates",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Art Gallery": {
            "description": "Create and showcase visual art including painting, drawing, and sculpture",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        }
    }
    
    # Clear and restore
    activities.clear()
    activities.update(original_activities)
    
    yield
