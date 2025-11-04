from sqlalchemy.orm import Session
from .. import models # .. means "go up one level" and import models
from .. import schemas
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

def search_foods_by_name(db: Session, name_query: str, limit: int = 10):
    """
    Searches for food items by name (case-insensitive)
    """
    # This is the core search logic:
    # 1. models.Food.name.ilike: 'ilike' means "case-insensitive LIKE"
    #    This is a powerful SQLAlchemy feature.
    # 2. f"%{name_query}%": The '%' are SQL wildcards.
    #    This finds any record where the 'name_query' string
    #    appears *anywhere* inside the food's name.

    search_pattern =f"%{name_query}%"

    return db.query(models.Food)\
            .filter(models.Food.name.ilike(search_pattern))\
            .limit(limit)\
            .all()
def create_food(db: Session, food: schemas.FoodCreate):
    """
    Creates a new food item in the database.
    
    Args:
        db: Database session
        food: FoodCreate schema with name and category_id
    
    Returns:
        The newly created Food object
    """
    # 1. Check if category exists
    category = db.query(models.FoodCategory).filter(
        models.FoodCategory.id == food.category_id
    ).first()
    
    if not category:
        return None  # Category doesn't exist
    
    # 2. Create the Food object
    db_food = models.Food(
        name=food.name,
        category_id=food.category_id
    )
    
    # 3. Add to database
    db.add(db_food)
    db.commit()  # Save to database
    db.refresh(db_food)  # Refresh to get the ID and relationships
    
    return db_food


def get_food_by_name(db: Session, name: str):
    """
    Check if a food with this exact name already exists.
    """
    return db.query(models.Food).filter(models.Food.name == name).first()