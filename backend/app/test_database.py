import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, Food, FoodCategory, UserProfile, FoodLog  # Fix: UserProfile not Profile

# Test database URL - SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Add sample food data for testing
    db = TestingSessionLocal()
    try:
        # Create food category
        if not db.query(FoodCategory).first():
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
    finally:
        db.close()

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
