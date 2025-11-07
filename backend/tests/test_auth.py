import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    # Add required fields for User model
    user_data = {
        **test_user_data,
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    # Check actual response format
    assert "user" in data
    assert "otp" in data
    assert data["user"]["email"] == test_user_data["email"]

def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test duplicate user registration"""
    # Add required fields
    user_data = {
        **test_user_data,
        "first_name": "Test",
        "last_name": "User"
    }
    
    # Register first time
    client.post("/auth/register", json=user_data)
    
    # Try to register again
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"].lower()

def test_register_invalid_email(client: TestClient):
    """Test registration with invalid email"""
    response = client.post("/auth/register", json={
        "email": "invalid-email",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 422

def test_register_weak_password(client: TestClient):
    """Test registration with weak password"""
    response = client.post("/auth/register", json={
        "email": "test2@example.com",
        "password": "123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 422
