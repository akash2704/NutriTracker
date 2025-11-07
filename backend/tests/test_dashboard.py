import pytest
from fastapi.testclient import TestClient
from tests.test_users import get_auth_token

def test_get_dashboard_no_data(client: TestClient, test_user_data):
    """Test dashboard with no logged food"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/dashboard/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "daily_nutrition" in data
    assert data["daily_nutrition"]["calories"] == 0

def test_get_dashboard_with_data(client: TestClient, test_user_data):
    """Test dashboard with logged food"""
    token = get_auth_token(client, test_user_data)
    
    # Log some food first
    foods_response = client.get("/foods/?search=rice&limit=1")
    foods = foods_response.json()
    
    if foods:
        food_id = foods[0]["id"]
        log_data = {
            "food_id": food_id,
            "quantity_g": 100,
            "meal_type": "breakfast"
        }
        client.post("/food-log/", json=log_data, headers={"Authorization": f"Bearer {token}"})
        
        # Get dashboard
        response = client.get("/dashboard/", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert "daily_nutrition" in data
        assert data["daily_nutrition"]["calories"] > 0

def test_get_dashboard_unauthorized(client: TestClient):
    """Test dashboard without authentication"""
    response = client.get("/dashboard/")
    assert response.status_code == 401

def test_dashboard_structure(client: TestClient, test_user_data):
    """Test dashboard response structure"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/dashboard/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "daily_nutrition" in data
    assert "weekly_average" in data
    assert "goal_progress" in data
    
    # Check daily nutrition structure
    daily = data["daily_nutrition"]
    assert "calories" in daily
    assert "protein" in daily
    assert "carbs" in daily
    assert "fat" in daily
