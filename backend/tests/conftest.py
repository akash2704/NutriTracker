import pytest
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.test_database import get_test_db, create_test_database

# Create test app without rate limiting
def create_test_app():
    from app.routers import general, foods, users, auth, foodLog, dashboard, profile, recipe, recommendations
    
    app = FastAPI(title="Test Nutrition Tracker API")
    
    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(general.router)
    app.include_router(foods.router) 
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(foodLog.router)
    app.include_router(dashboard.router)
    app.include_router(profile.router)
    app.include_router(recipe.router)
    app.include_router(recommendations.router)
    
    return app

# Override database dependency
test_app = create_test_app()
test_app.dependency_overrides[get_db] = get_test_db

@pytest.fixture(scope="session")
def client():
    create_test_database()
    with TestClient(test_app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture(scope="function")
def test_profile_data():
    return {
        "birth_date": "1990-01-01",
        "gender": "male",
        "height_cm": 175,
        "weight_kg": 70,
        "activity_level": "moderate",
        "dietary_preference": "vegetarian",
        "budget_range": "medium"
    }
