from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # To return a list of foods

from .. import schemas  # Import our Pydantic schemas
from .. import services # Import our new service
from ..database import get_db # Import our DB session-getter

router = APIRouter(
    prefix="/foods", # All routes in this file will start with /foods
    tags=["Foods"]    # This groups them in the /docs
)

@router.get("/", response_model=List[schemas.Food])
def read_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all food items from the database with pagination.
    """
    foods = services.get_foods(db, skip=skip, limit=limit)
    return foods

@router.get("/{food_id}", response_model=schemas.Food)
def read_food(food_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single food item by its ID.
    
    - **food_id**: The 'Path Parameter' from the URL.
    - **db: Session = Depends(get_db)**: This is FastAPI's
      Dependency Injection. It runs 'get_db()' and gives us
      a database session.
    - **response_model=schemas.Food**: This tells FastAPI to
      filter the output to *only* match our 'Food' schema.
    """
    
    # 1. Ask the "service" (kitchen) for the food
    food = services.get_food_by_id(db, food_id=food_id)
    
    # 2. Handle the "Not Found" case
    if food is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Food not found"
        )
    
    # 3. Return the food
    return food
