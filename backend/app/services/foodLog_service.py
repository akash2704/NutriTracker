from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from datetime import datetime, date, timezone
from typing import List

def create_log_entry(db: Session, log_in: schemas.LogCreate, user_id: int) -> models.FoodLog:
    """
    Business logic for creating a new food log entry.
    """
    
    # 1. Validate that the food item exists
    food = db.query(models.Food).filter(models.Food.id == log_in.food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food with id {log_in.food_id} not found."
        )
        
    # 2. Create the new FoodLog object
    #    We use **log_in.model_dump() to unpack all fields from the schema
    db_log_entry = models.FoodLog(
        **log_in.model_dump(),
        user_id=user_id,
        created_at=datetime.utcnow() # Manually set creation time
    )
    
    # 3. Add to database, commit, and refresh
    db.add(db_log_entry)
    db.commit()
    db.refresh(db_log_entry)
    
    # 4. Return the newly created object
    # The 'food' relationship will be auto-populated by SQLAlchemy
    return db_log_entry

def get_food_logs(db: Session, user_id: int, log_date: date = None) -> List[schemas.FoodLogResponse]:
    """Get food logs for a user on a specific date"""
    if log_date is None:
        log_date = datetime.now(timezone.utc).date()
    
    logs = db.query(models.FoodLog).filter(
        models.FoodLog.user_id == user_id,
        models.FoodLog.log_date == log_date
    ).all()
    
    result = []
    for log in logs:
        # Get calories from food nutrients
        calories = 0
        for nutrient in log.food.nutrients:
            if nutrient.nutrient.name == "Energy":
                calories = nutrient.value_per_100g * (log.quantity_grams / 100)
                break
        
        result.append(schemas.FoodLogResponse(
            id=log.id,
            food_name=log.food.name,
            quantity_grams=log.quantity_grams,
            meal_type=log.meal_type,
            calories=round(calories, 1)
        ))
    
    return result
