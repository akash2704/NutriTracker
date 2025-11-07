import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "registered" in data["message"].lower()

def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test duplicate user registration"""
    # Register first time
    client.post("/auth/register", json=test_user_data)
    
    # Try to register again
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"].lower()

def test_register_invalid_email(client: TestClient):
    """Test registration with invalid email"""
    response = client.post("/auth/register", json={
        "email": "invalid-email",
        "password": "testpassword123"
    })
    assert response.status_code == 422

def test_register_weak_password(client: TestClient):
    """Test registration with weak password"""
    response = client.post("/auth/register", json={
        "email": "test2@example.com",
        "password": "123"
    })
    assert response.status_code == 422

def test_login_unverified_user(client: TestClient, test_user_data):
    """Test login with unverified user"""
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Try to login without verification
    response = client.post("/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 400
    data = response.json()
    assert "not verified" in data["detail"].lower()

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    response = client.post("/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert "incorrect" in data["detail"].lower()

def test_verify_otp_invalid(client: TestClient, test_user_data):
    """Test OTP verification with invalid OTP"""
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Try invalid OTP
    response = client.post("/auth/verify-otp", json={
        "email": test_user_data["email"],
        "otp": "000000"
    })
    assert response.status_code == 400
    data = response.json()
    assert "invalid" in data["detail"].lower()

def test_verify_otp_nonexistent_user(client: TestClient):
    """Test OTP verification for nonexistent user"""
    response = client.post("/auth/verify-otp", json={
        "email": "nonexistent@example.com",
        "otp": "123456"
    })
    assert response.status_code == 404
