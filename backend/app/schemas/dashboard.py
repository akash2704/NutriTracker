from pydantic import BaseModel
from datetime import date
from typing import List

# This schema defines a single row in our final report
class NutrientReport(BaseModel):
    nutrient_name: str
    unit: str
    goal: float
    consumed: float
    gap: float # The difference (consumed - goal)

# This is the main object our API will return
class DashboardResponse(BaseModel):
    log_date: date
    matched_demographic_group: str
    
    # We will have a summary for the "big 4" nutrients
    total_calories_goal: float
    total_calories_consumed: float
    total_protein_goal: float
    total_protein_consumed: float
    total_fat_goal: float
    total_fat_consumed: float
    total_carbs_goal: float
    total_carbs_consumed: float
    
    # And a detailed breakdown of all nutrients
    detailed_analysis: List[NutrientReport]

    class Config:
        orm_mode = True

