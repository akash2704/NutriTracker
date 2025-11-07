import pytest
from fastapi.testclient import TestClient
from tests.test_users import get_auth_token

def test_get_recommendations_no_profile(client: TestClient, test_user_data):
    """Test recommendations without profile"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/recommendations/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_get_recommendations_with_profile(client: TestClient, test_user_data, test_profile_data):
    """Test recommendations with profile"""
    token = get_auth_token(client, test_user_data)
    
    # Create profile first
    client.post("/profile/me", json=test_profile_data, headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/recommendations/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "bmr" in data
    assert "tdee" in data
    assert "target_calories" in data
    assert "bmi" in data
    assert "recommendations" in data

def test_get_recommendations_unauthorized(client: TestClient):
    """Test recommendations without authentication"""
    response = client.get("/recommendations/")
    assert response.status_code == 401

def test_recommendations_structure(client: TestClient, test_user_data, test_profile_data):
    """Test recommendations response structure"""
    token = get_auth_token(client, test_user_data)
    
    # Create profile
    client.post("/profile/me", json=test_profile_data, headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/recommendations/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    
    # Check numeric values are positive
    assert data["bmr"] > 0
    assert data["tdee"] > 0
    assert data["target_calories"] > 0
    assert data["bmi"] > 0
    
    # Check recommendations structure
    recs = data["recommendations"]
    assert "greeting" in recs
    assert "meal_plan" in recs
    assert "exercise_plan" in recs
    
    # Check meal plan structure
    meal_plan = recs["meal_plan"]
    assert "breakfast" in meal_plan
    assert "lunch" in meal_plan
    assert "dinner" in meal_plan
    assert "snack" in meal_plan
