import pytest
from fastapi.testclient import TestClient
from tests.test_users import get_auth_token

def test_get_recommendations_no_profile(client: TestClient, test_user_data):
    """Test recommendations without profile"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/recommendations/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_get_recommendations_unauthorized(client: TestClient):
    """Test recommendations without authentication"""
    response = client.get("/recommendations/")
    assert response.status_code == 401

def test_get_recommendations_with_profile_fallback(client: TestClient, test_user_data, test_profile_data):
    """Test recommendations with profile - should get fallback response (no Gemini API call)"""
    token = get_auth_token(client, test_user_data)
    
    # Create profile first
    client.post("/profile/me", json=test_profile_data, headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/recommendations/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    
    # Check basic structure (should get fallback response)
    assert "bmr" in data
    assert "tdee" in data
    assert "target_calories" in data
    assert "bmi" in data
    
    # Should have fallback recommendations
    assert "recommendations" in data
    recs = data["recommendations"]
    assert "meal_plan" in recs
