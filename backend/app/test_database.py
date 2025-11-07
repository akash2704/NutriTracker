import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import Base and ALL models to ensure they're registered
from app.models import (
    Base, User, Food, FoodCategory, UserProfile, FoodLog, 
    Nutrient, FoodNutrient, DemographicGroup, RDA
)

# Test database URL - SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_database():
    # Drop all tables first, then create them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Add sample food data for testing
    db = TestingSessionLocal()
    try:
        # Create food category
        category = FoodCategory(id=1, name="Test Foods")
        db.add(category)
        db.commit()
        
        # Add sample foods
        foods = [
            Food(id=1, name="Rice", category_id=1),
            Food(id=2, name="Wheat", category_id=1),
        ]
        db.add_all(foods)
        db.commit()
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
