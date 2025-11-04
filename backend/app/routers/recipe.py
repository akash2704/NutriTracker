from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db
from ..dependencies import get_current_user
from ..services.recipe_parser import parse_recipe_text
from pydantic import BaseModel

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"],
    dependencies=[Depends(get_current_user)]
)

class RecipeRequest(BaseModel):
    recipe_text: str

class RecipeIngredient(BaseModel):
    ingredient: str
    quantity: float
    unit: str
    grams: float
    food_id: int = None
    food_name: str = None

class RecipeResponse(BaseModel):
    ingredients: List[RecipeIngredient]
    total_calories: float = 0

@router.post("/parse", response_model=RecipeResponse)
def parse_recipe(
    request: RecipeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Parse natural language recipe into ingredients"""
    ingredients = parse_recipe_text(db, request.recipe_text)
    
    response_ingredients = []
    total_calories = 0
    
    for ing in ingredients:
        if ing:
            ingredient_data = {
                'ingredient': ing['ingredient'],
                'quantity': ing['quantity'],
                'unit': ing['unit'],
                'grams': ing['grams'],
                'food_id': ing['food_id'],
                'food_name': ing['food'].name if ing['food'] else None
            }
            response_ingredients.append(ingredient_data)
            
            # Calculate calories if food found
            if ing['food']:
                # Assuming 100g base nutrition data
                calories_per_100g = 200  # Default estimate
                total_calories += (ing['grams'] / 100) * calories_per_100g
    
    return {
        'ingredients': response_ingredients,
        'total_calories': total_calories
    }
