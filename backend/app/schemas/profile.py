import enum
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from ..models import GenderEnum, ActivityLevelEnum

# --- THIS IS THE FIX ---
# We define the *base* class first.
class ProfileBase(BaseModel):
    birth_date: date = Field(..., description="User's date of birth")
    gender: GenderEnum = Field(..., description="User's gender")
    activity_level: ActivityLevelEnum = Field(..., description="User's typical activity level")
    height_cm: float = Field(..., gt=0, description="User's height in centimeters")
    weight_kg: float = Field(..., gt=0, description="User's weight in kilograms")
    dietary_preference: Optional[str] = Field(None, description="Dietary preference: vegetarian, non-vegetarian, vegan")
    budget_range: Optional[str] = Field(None, description="Budget range: low, medium, high")
    preferred_cuisine: Optional[str] = Field(None, description="Preferred cuisine: indian, continental, mixed")
# --- END OF FIX ---

# This schema defines the data the user will *send* to us.
# It inherits the base fields.
class ProfileCreate(ProfileBase):
    pass # No extra fields needed

# This schema defines the data we will *return* to the user.
# It inherits the base fields and adds new ones.
class Profile(ProfileBase):
    user_id: int
    demographic_group_id: int | None = Field(None, description="The ID of the matched NIN demographic group")
    
    class Config:
        from_attributes = True # Pydantic v2 alias for orm_mode