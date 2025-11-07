import pytest
from fastapi.testclient import TestClient
from tests.test_users import get_auth_token

def test_parse_recipe_text(client: TestClient, test_user_data):
    """Test parsing recipe from text"""
    token = get_auth_token(client, test_user_data)
    
    recipe_data = {
        "recipe_text": "Ingredients: 1 cup rice, 2 cups water, 1 tsp salt. Instructions: Boil water, add rice and salt, cook for 20 minutes."
    }
    
    response = client.post("/recipe/parse", 
                          json=recipe_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "ingredients" in data
    assert "total_nutrition" in data

def test_parse_recipe_unauthorized(client: TestClient):
    """Test parsing recipe without authentication"""
    recipe_data = {
        "recipe_text": "Ingredients: 1 cup rice, 2 cups water"
    }
    
    response = client.post("/recipe/parse", json=recipe_data)
    assert response.status_code == 401

def test_parse_recipe_empty_text(client: TestClient, test_user_data):
    """Test parsing empty recipe text"""
    token = get_auth_token(client, test_user_data)
    
    recipe_data = {
        "recipe_text": ""
    }
    
    response = client.post("/recipe/parse", 
                          json=recipe_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_parse_recipe_invalid_format(client: TestClient, test_user_data):
    """Test parsing recipe with invalid format"""
    token = get_auth_token(client, test_user_data)
    
    recipe_data = {
        "recipe_text": "This is not a recipe format"
    }
    
    response = client.post("/recipe/parse", 
                          json=recipe_data,
                          headers={"Authorization": f"Bearer {token}"})
    # Should still return 200 but with empty or minimal data
    assert response.status_code in [200, 400]
