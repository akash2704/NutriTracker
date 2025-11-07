import pytest
from fastapi.testclient import TestClient

def get_auth_token(client: TestClient, user_data):
    """Helper function to get auth token"""
    # Register and verify user
    client.post("/auth/register", json=user_data)
    
    # Mock verification by directly updating database
    from app.test_database import TestingSessionLocal
    from app.models import User
    
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == user_data["email"]).first()
    if user:
        user.is_verified = True
        user.otp = "123456"  # Set a known OTP
        db.commit()
    db.close()
    
    # Verify with known OTP
    client.post("/auth/verify-otp", json={
        "email": user_data["email"],
        "otp": "123456"
    })
    
    # Login to get token
    response = client.post("/auth/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    return response.json()["access_token"]

def test_get_current_user(client: TestClient, test_user_data):
    """Test getting current user info"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert "id" in data

def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without token"""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token"""
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_create_profile(client: TestClient, test_user_data, test_profile_data):
    """Test creating user profile"""
    token = get_auth_token(client, test_user_data)
    
    response = client.post("/profile/me", 
                          json=test_profile_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["gender"] == test_profile_data["gender"]
    assert data["height_cm"] == test_profile_data["height_cm"]

def test_get_profile(client: TestClient, test_user_data, test_profile_data):
    """Test getting user profile"""
    token = get_auth_token(client, test_user_data)
    
    # Create profile first
    client.post("/profile/me", 
                json=test_profile_data,
                headers={"Authorization": f"Bearer {token}"})
    
    # Get profile
    response = client.get("/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["gender"] == test_profile_data["gender"]

def test_get_profile_not_found(client: TestClient, test_user_data):
    """Test getting profile that doesn't exist"""
    token = get_auth_token(client, test_user_data)
    
    response = client.get("/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_create_profile_invalid_data(client: TestClient, test_user_data):
    """Test creating profile with invalid data"""
    token = get_auth_token(client, test_user_data)
    
    invalid_data = {
        "birth_date": "invalid-date",
        "gender": "invalid",
        "height_cm": -10,
        "weight_kg": -5
    }
    
    response = client.post("/profile/me", 
                          json=invalid_data,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
