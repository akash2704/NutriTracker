import enum
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Date, 
    Enum # We still use this for Gender/Activity
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# This is the Pydantic/Python Enum. Our schemas will use this.
class MealTypeEnum(str, enum.Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"

Base = declarative_base()

# --- USER MODELS ---

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class ActivityLevelEnum(str, enum.Enum):
    sedentary = "sedentary"
    moderate = "moderate"
    heavy = "heavy"
    pregnant = "pregnant"
    lactating_0_6 = "lactating_0-6"
    lactating_6_12 = "lactating_6-12"
    infant = "infant"
    child = "child"
    adolescent = "adolescent"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=False)
    
    verification_otp = Column(String(10), nullable=True)
    otp_expires_at = Column(DateTime(timezone=True), nullable=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    food_logs = relationship("FoodLog", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    birth_date = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    activity_level = Column(Enum(ActivityLevelEnum), nullable=True)
    
    # New fields for recommendations
    dietary_preference = Column(String(20), nullable=True)  # vegetarian, non-vegetarian, vegan
    budget_range = Column(String(20), nullable=True)  # low, medium, high
    preferred_cuisine = Column(String(50), nullable=True)  # indian, continental, mixed
    
    demographic_group_id = Column(Integer, ForeignKey("demographic_groups.id"), nullable=True)
    
    user = relationship("User", back_populates="profile")
    demographic_group = relationship("DemographicGroup")

# --- FOOD & NUTRIENT MODELS ---

class FoodCategory(Base):
    __tablename__ = "food_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    foods = relationship("Food", back_populates="category")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("food_categories.id"))
    
    category = relationship("FoodCategory", back_populates="foods")
    nutrients = relationship("FoodNutrient", back_populates="food", cascade="all, delete-orphan")
    logs = relationship("FoodLog", back_populates="food")

class Nutrient(Base):
    __tablename__ = "nutrients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    unit = Column(String(20), nullable=False) # e.g., 'g', 'mg', 'µg'
    
    food_associations = relationship("FoodNutrient", back_populates="nutrient")
    rda_associations = relationship("RDA", back_populates="nutrient")

class FoodNutrient(Base):
    __tablename__ = "food_nutrients"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    nutrient_id = Column(Integer, ForeignKey("nutrients.id"), nullable=False)
    value_per_100g = Column(Float, nullable=False)
    
    food = relationship("Food", back_populates="nutrients")
    nutrient = relationship("Nutrient", back_populates="food_associations")

# --- RDA ("GOAL") MODELS ---

class DemographicGroup(Base):
    __tablename__ = "demographic_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    
    gender = Column(Enum(GenderEnum), nullable=True)
    activity_level = Column(Enum(ActivityLevelEnum), nullable=True)
    age_min_years = Column(Float, nullable=False)
    age_max_years = Column(Float, nullable=False)
    
    rda_values = relationship("RDA", back_populates="demographic_group", cascade="all, delete-orphan")

class RDA(Base):
    __tablename__ = "rda"
    id = Column(Integer, primary_key=True, index=True)
    demographic_group_id = Column(Integer, ForeignKey("demographic_groups.id"), nullable=False)
    nutrient_id = Column(Integer, ForeignKey("nutrients.id"), nullable=False)
    recommended_value = Column(Float, nullable=False)
    
    demographic_group = relationship("DemographicGroup", back_populates="rda_values")
    nutrient = relationship("Nutrient", back_populates="rda_associations")

# --- TRACKER MODELS ---

class FoodLog(Base):
    __tablename__ = "food_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity_grams = Column(Float, nullable=False)
    log_date = Column(Date, nullable=False, index=True)
    
    # --- THIS IS THE "NO-HASSLE" FIX ---
    # Instead of a complex database Enum, we just use a simple String.
    # Our Pydantic schema will still validate this, so our app is safe.
    meal_type = Column(String(50), nullable=False)
    # --- END OF FIX ---
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="food_logs")
    food = relationship("Food", back_populates="logs")

