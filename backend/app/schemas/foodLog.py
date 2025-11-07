from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from enum import Enum
from .food import Food  # Import the schema we'll use for nesting

# 1. Create an Enum for Meal Types for data consistency
class MealTypeEnum(str, Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"

# 2. Base Schema: The core fields for a log entry
class LogBase(BaseModel):
    food_id: int
    quantity_grams: float
    log_date: date
    meal_type: MealTypeEnum

# 3. Create Schema: This is what the user will send to our API
#    It's exactly the same as the base for this model.
class LogCreate(LogBase):
    pass

# 4. Response Schema: This is what our API will return
#    It includes the database-generated fields (id, user_id, created_at)
#    and the nested 'food' object for context.
class Log(LogBase):
    id: int
    user_id: int
    created_at: datetime
    
    # This "magic" field will be populated automatically by SQLAlchemy
    # It will contain the full Food object associated with this log.
    food: Food 
    
    # This tells Pydantic to read the data even if it's
    # a SQLAlchemy model object (not just a dict).
    model_config = ConfigDict(from_attributes=True)

# 5. Food Log Response Schema for dashboard display
class FoodLogResponse(BaseModel):
    id: int
    food_name: str
    quantity_grams: float
    meal_type: str
    calories: float
    
    model_config = ConfigDict(from_attributes=True)

