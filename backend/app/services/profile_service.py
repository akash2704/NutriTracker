from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas # We import both

def _calculate_age(birth_date: date) -> float:
    """Helper function to calculate age from a date of birth."""
    today = date.today()
    # This logic correctly handles leap years and birth dates yet to occur this year
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Handle infants (e.g., 6 months = 0.5 years)
    if age == 0:
        return (today - birth_date).days / 365.25
    return float(age)

# --- THIS IS THE FIX ---
# The type hints for gender and activity now correctly point to 'models'
def _match_demographic_group(db: Session, age: float, gender: models.GenderEnum, activity: models.ActivityLevelEnum) -> models.DemographicGroup | None:
# --- END OF FIX ---
    """
    Finds the correct NIN DemographicGroup based on user's stats.
    """
    query = db.query(models.DemographicGroup).filter(
        models.DemographicGroup.age_min_years <= age,
        models.DemographicGroup.age_max_years >= age,
        models.DemographicGroup.activity_level == activity
    )
    
    # Handle non-gender-specific groups (infants, children)
    # or gender-specific groups (adults, adolescents)
    if gender != models.GenderEnum.other:
        # User has a specific gender, so we can match on 'male'/'female' OR 'None' (for children)
        query = query.filter(
            (models.DemographicGroup.gender == gender) | 
            (models.DemographicGroup.gender == None)
        )
    
    matched_group = query.first()
    return matched_group

def create_or_update_profile(db: Session, current_user: models.User, profile_in: schemas.ProfileCreate) -> models.UserProfile:
    """
    Creates or updates a user's profile.
    This is the core logic that calculates age and finds the
    matching demographic group for RDA calculations.
    """
    
    # 1. Calculate age
    age = _calculate_age(profile_in.birth_date)
    
    # 2. Find the matching DemographicGroup
    #    (profile_in.gender and profile_in.activity_level are already the correct Enum types
    #    thanks to our Pydantic schema)
    matched_group = _match_demographic_group(db, age, profile_in.gender, profile_in.activity_level)
    
    if not matched_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not find a matching demographic group for the provided stats. Age: {age}"
        )

    # 3. Check if a profile exists, or create a new one (upsert logic)
    profile = current_user.profile
    if not profile:
        profile = models.UserProfile(user_id=current_user.id)
        db.add(profile)

    # 4. Update the profile with the new data
    profile.birth_date = profile_in.birth_date
    profile.gender = profile_in.gender
    profile.activity_level = profile_in.activity_level
    profile.height_cm = profile_in.height_cm
    profile.weight_kg = profile_in.weight_kg
    profile.dietary_preference = profile_in.dietary_preference
    profile.budget_range = profile_in.budget_range
    profile.preferred_cuisine = profile_in.preferred_cuisine
    
    # 5. This is the most important part:
    # We "cache" the matched group ID on the profile.
    # The dashboard will now read this ID.
    profile.demographic_group_id = matched_group.id

    try:
        db.commit()
        db.refresh(profile)
        return profile
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the profile: {str(e)}"
        )

def get_profile(db: Session, current_user: models.User) -> models.UserProfile:
    """
    Fetches the current user's profile.
    """
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please create your profile."
        )
    return current_user.profile