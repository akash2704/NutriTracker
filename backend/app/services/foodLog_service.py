from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from datetime import datetime

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
