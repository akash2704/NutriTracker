import pytest
from fastapi.testclient import TestClient

def test_search_foods(client: TestClient):
    """Test food search functionality"""
    response = client.get("/foods/?search=rice&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_search_foods_no_query(client: TestClient):
    """Test food search without query"""
    response = client.get("/foods/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_foods_empty_result(client: TestClient):
    """Test food search with no results"""
    response = client.get("/foods/?search=nonexistentfood12345")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_food_by_id(client: TestClient):
    """Test getting food by ID"""
    # First get a food from search
    search_response = client.get("/foods/?search=rice&limit=1")
    foods = search_response.json()
    
    if foods:
        food_id = foods[0]["id"]
        response = client.get(f"/foods/{food_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == food_id
        assert "name" in data
        assert "calories_per_100g" in data

def test_get_food_invalid_id(client: TestClient):
    """Test getting food with invalid ID"""
    response = client.get("/foods/99999")
    assert response.status_code == 404

def test_search_foods_with_limit(client: TestClient):
    """Test food search with limit parameter"""
    response = client.get("/foods/?search=rice&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 3

def test_search_foods_invalid_limit(client: TestClient):
    """Test food search with invalid limit"""
    response = client.get("/foods/?search=rice&limit=-1")
    assert response.status_code == 422
