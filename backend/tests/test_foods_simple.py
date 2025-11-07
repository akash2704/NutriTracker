import pytest
from fastapi.testclient import TestClient

def test_search_foods_basic(client: TestClient):
    """Test basic food search functionality"""
    response = client.get("/foods/?search=rice&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_food_by_id_basic(client: TestClient):
    """Test getting food by ID"""
    response = client.get("/foods/1")
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "category_id" in data
        # Note: Food model doesn't have direct nutrition fields
        # Nutrition data is in separate FoodNutrient table
    else:
        # If no food found, should return 404
        assert response.status_code == 404

def test_foods_endpoint_exists(client: TestClient):
    """Test that foods endpoint exists and responds"""
    response = client.get("/foods/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
