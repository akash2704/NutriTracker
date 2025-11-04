from sqlalchemy.orm import Session
from .. import models # .. means "go up one level" and import models

def get_food_by_id(db: Session, food_id: int):
    """
    Fetches a single food item by its ID.
    
    This is the "business logic" - the actual database query.
    """
    return db.query(models.Food).filter(models.Food.id == food_id).first()

def get_foods(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of all foods, with pagination.
    """
    return db.query(models.Food).offset(skip).limit(limit).all()