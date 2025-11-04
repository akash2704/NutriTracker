from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional # To return a list of foods

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

@router.get("/search", response_model=List[schemas.Food])
def search_foods(
    q: Optional[str] = None,  # 'q' for "query". Optional[str] means it's not required
    limit: int = 10,          # Default to 10 results
    db: Session = Depends(get_db)
):
    """
    Search for food items by name.
    
    - **q**: The search query string.
    - **limit**: The maximum number of results to return.
    """
    if q:
        # This is where it calls your new service function
        foods = services.search_foods_by_name(db, name_query=q, limit=limit)
    else:
        # If no query 'q' is given, just return an empty list
        foods = []
        
    # Note: A search that finds nothing is NOT an error.
    # It's a successful search that returned 0 results.
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
@router.post("/", response_model=schemas.Food, status_code=status.HTTP_201_CREATED)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    """
    Create a new food item.
    
    - **name**: The name of the food (must be unique)
    - **category_id**: The ID of the food category this belongs to
    
    Returns the newly created food with its ID and category details.
    """
    # 1. Check if food with this name already exists
    existing_food = services.get_food_by_name(db, name=food.name)
    if existing_food:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Food with name '{food.name}' already exists"
        )
    
    # 2. Try to create the food
    db_food = services.create_food(db, food=food)
    
    # 3. Handle case where category doesn't exist
    if db_food is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food category with id {food.category_id} not found"
        )
    
    # 4. Return the created food
    return db_food
