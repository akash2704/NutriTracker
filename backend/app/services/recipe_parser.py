import re
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ..models import Food

class RecipeParser:
    def __init__(self, db: Session):
        self.db = db
        self.quantity_patterns = [
            r'(\d+(?:\.\d+)?)\s*(cups?|cup)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(tbsp|tablespoons?|tablespoon)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(tsp|teaspoons?|teaspoon)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(grams?|g)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(kg|kilograms?)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(ml|milliliters?)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(liters?|l)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s+(.+)',  # Just number + ingredient
        ]
        
        self.unit_conversions = {
            'cup': 240,  # ml to grams (approximate)
            'cups': 240,
            'tbsp': 15,
            'tablespoon': 15,
            'tablespoons': 15,
            'tsp': 5,
            'teaspoon': 5,
            'teaspoons': 5,
            'g': 1,
            'grams': 1,
            'gram': 1,
            'kg': 1000,
            'kilograms': 1000,
            'kilogram': 1000,
            'ml': 1,  # Assume 1ml = 1g for liquids
            'milliliters': 1,
            'milliliter': 1,
            'l': 1000,
            'liters': 1000,
            'liter': 1000,
        }

    def parse_recipe(self, recipe_text: str) -> List[Dict]:
        """Parse natural language recipe into ingredients with quantities"""
        lines = recipe_text.strip().split('\n')
        ingredients = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parsed = self._parse_ingredient_line(line)
            if parsed:
                ingredients.append(parsed)
                
        return ingredients

    def _parse_ingredient_line(self, line: str) -> Dict:
        """Parse a single ingredient line"""
        line = line.lower().strip()
        
        for pattern in self.quantity_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3:
                    quantity, unit, ingredient = match.groups()
                    grams = self._convert_to_grams(float(quantity), unit)
                else:
                    quantity, ingredient = match.groups()
                    grams = float(quantity)  # Assume grams if no unit
                
                # Find matching food in database
                food = self._find_food(ingredient.strip())
                
                return {
                    'ingredient': ingredient.strip(),
                    'quantity': float(quantity),
                    'unit': unit if len(match.groups()) == 3 else 'g',
                    'grams': grams,
                    'food': food,
                    'food_id': food.id if food else None
                }
        
        return None

    def _convert_to_grams(self, quantity: float, unit: str) -> float:
        """Convert quantity to grams"""
        unit = unit.lower()
        conversion = self.unit_conversions.get(unit, 1)
        return quantity * conversion

    def _find_food(self, ingredient: str) -> Food:
        """Find best matching food in database"""
        # Try exact match first
        food = self.db.query(Food).filter(
            Food.name.ilike(f"%{ingredient}%")
        ).first()
        
        if not food:
            # Try partial matches
            words = ingredient.split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    food = self.db.query(Food).filter(
                        Food.name.ilike(f"%{word}%")
                    ).first()
                    if food:
                        break
        
        return food

def parse_recipe_text(db: Session, recipe_text: str) -> List[Dict]:
    """Parse recipe and return ingredients with nutritional info"""
    parser = RecipeParser(db)
    return parser.parse_recipe(recipe_text)
