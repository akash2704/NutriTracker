import pytest
from fastapi.testclient import TestClient
from tests.test_users import get_auth_token

def test_log_food(client: TestClient, test_user_data):
    """Test logging food intake"""
    token = get_auth_token(client, test_user_data)
    
    # Get a food ID first
    foods_response = client.get("/foods/?search=rice&limit=1")
    foods = foods_response.json()
    
    if foods:
        food_id = foods[0]["id"]
        
        log_data = {
            "food_id": food_id,
            "quantity_g": 100,
            "meal_type": "breakfast"
        }
        
        response = client.post("/food-log/", 
                              json=log_data,
                              headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

def test_log_food_unauthorized(client: TestClient):
    """Test logging food without authentication"""
    log_data = {
        "food_id": 1,
        "quantity_g": 100,
        "meal_type": "breakfast"
    }
    
    response = client.post("/food-log/", json=log_data)
    assert response.status_code == 401

def test_log_food_invalid_food_id(client: TestClient, test_user_data):
    """Test logging food with invalid food ID"""
    token = get_auth_token(client, test_user_data)
    
    log_data = {
        "food_id": 99999,
        "quantity_g": 100,
        "meal_type": "breakfast"
    }
    
    response = client.post("/food-log/", 
                          json=log_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_log_food_invalid_quantity(client: TestClient, test_user_data):
    """Test logging food with invalid quantity"""
    token = get_auth_token(client, test_user_data)
    
    log_data = {
        "food_id": 1,
        "quantity_g": -10,
        "meal_type": "breakfast"
    }
    
    response = client.post("/food-log/", 
                          json=log_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422

def test_log_food_invalid_meal_type(client: TestClient, test_user_data):
    """Test logging food with invalid meal type"""
    token = get_auth_token(client, test_user_data)
    
    log_data = {
        "food_id": 1,
        "quantity_g": 100,
        "meal_type": "invalid_meal"
    }
    
    response = client.post("/food-log/", 
                          json=log_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
