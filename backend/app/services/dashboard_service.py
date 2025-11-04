from sqlalchemy.orm import Session
from datetime import date, datetime, timezone
from collections import defaultdict
from fastapi import HTTPException, status
from .. import models, schemas

def _calculate_age(birth_date: date) -> int:
    """Calculates a user's age from their birth_date."""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def _get_user_profile(db: Session, user: models.User) -> models.UserProfile:
    """Fetches a user's profile and validates it."""
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please create your profile."
        )
    
    if not all([profile.birth_date, profile.gender, profile.activity_level, profile.weight_kg]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile is incomplete. Please set birth_date, gender, activity_level, and weight_kg."
        )
    return profile

def _get_demographic_group(db: Session, profile: models.UserProfile, age: int) -> models.DemographicGroup:
    """Matches a user's profile stats to a DemographicGroup in the database."""
    
    # Handle the simple, non-gendered groups first
    if age < 18:
        group_name_map = {
            (0, 0.5): "Infants 0-6 months",
            (0.5, 1): "Infants 6-12 months",
            (1, 3): "Children 1-3 years",
            (4, 6): "Children 4-6 years",
            (7, 9): "Children 7-9 years",
            (10, 12): "Boys 10-12 years" if profile.gender == 'male' else "Girls 10-12 years",
            (13, 15): "Boys 13-15 years" if profile.gender == 'male' else "Girls 13-15 years",
            (16, 17): "Boys 16-17 years" if profile.gender == 'male' else "Girls 16-17 years",
        }
        
        for (age_min, age_max), name in group_name_map.items():
            if age_min <= age <= age_max:
                group = db.query(models.DemographicGroup).filter_by(name=name).first()
                if group: return group

    # Handle adult groups
    else:
        group = db.query(models.DemographicGroup).filter(
            models.DemographicGroup.gender == profile.gender,
            models.DemographicGroup.activity_level == profile.activity_level,
            models.DemographicGroup.age_min_years <= age,
            models.DemographicGroup.age_max_years >= age
        ).first()
        if group: return group

    raise HTTPException(status_code=404, detail="Could not match your profile to a demographic group.")

def _get_rda_goal(db: Session, group: models.DemographicGroup, profile: models.UserProfile) -> dict:
    """
    Fetches the RDA "Goal" for the matched group and applies BMI-based modifiers.
    Returns a dictionary map: {nutrient_name: goal_value}
    """
    rda_goals = {}
    
    # 1. Fetch all standard RDA values for this group
    rda_entries = db.query(models.RDA).filter_by(demographic_group_id=group.id).all()
    for entry in rda_entries:
        rda_goals[entry.nutrient.name] = entry.recommended_value
        
    # 2. Apply "Smart" Modifiers (as we discussed)
    if profile.height_cm and profile.weight_kg and profile.height_cm > 0:
        height_m = profile.height_cm / 100
        bmi = profile.weight_kg / (height_m * height_m)
        
        # Get the baseline energy goal
        base_energy_goal = rda_goals.get("Energy", 2000) # Default to 2000 if not found
        
        if bmi > 25: # Overweight
            # Set a 500 kcal deficit for weight loss
            rda_goals["Energy"] = base_energy_goal - 500
        elif bmi < 18.5: # Underweight
            # Set a 300 kcal surplus for weight gain
            rda_goals["Energy"] = base_energy_goal + 300
        # Else: (18.5-25) - Healthy weight, no change to energy goal
            
    return rda_goals

def _get_consumption(db: Session, user: models.User, log_date: date) -> defaultdict:
    """
    Calculates the total "Score" (nutrient consumption) for a user on a specific date.
    Returns a dictionary map: {nutrient_name: consumed_value}
    """
    
    # Find all logs for this user on this day
    logs = db.query(models.FoodLog).filter(
        models.FoodLog.user_id == user.id,
        models.FoodLog.log_date == log_date
    ).all()
    
    # Use defaultdict to automatically handle new keys
    total_consumption = defaultdict(float)
    
    for log in logs:
        # Get the scaling factor (e.g., 150g logged / 100g base = 1.5)
        scale_factor = log.quantity_grams / 100.0
        
        # Get all nutrients for the food in this log
        # We use .food to access the relationship
        for fn in log.food.nutrients:
            nutrient_name = fn.nutrient.name
            base_value = fn.value_per_100g
            
            # Calculate the consumed value and add to our total
            consumed_value = base_value * scale_factor
            total_consumption[nutrient_name] += consumed_value
            
    return total_consumption

def get_dashboard_data(db: Session, user: models.User, log_date: date) -> schemas.DashboardResponse:
    """
    Main service function to orchestrate the entire gap analysis.
    """
    
    # 1. Get User Profile & Age
    profile = _get_user_profile(db, user)
    age = _calculate_age(profile.birth_date)
    
    # 2. Get "Goal" (RDA)
    demographic_group = _get_demographic_group(db, profile, age)
    rda_goals = _get_rda_goal(db, demographic_group, profile)
    
    # 3. Get "Score" (Consumption)
    total_consumption = _get_consumption(db, user, log_date)
    
    # 4. Combine & Calculate "Gap"
    analysis_report: List[schemas.NutrientReport] = []
    
    # Get a master list of all nutrients we have a goal for
    all_goal_nutrients = db.query(models.Nutrient).filter(
        models.Nutrient.name.in_(rda_goals.keys())
    ).all()

    for nutrient in all_goal_nutrients:
        name = nutrient.name
        goal_val = rda_goals.get(name, 0.0)
        consumed_val = total_consumption.get(name, 0.0)
        
        analysis_report.append(
            schemas.NutrientReport(
                nutrient_name=name,
                unit=nutrient.unit,
                goal=round(goal_val, 2),
                consumed=round(consumed_val, 2),
                gap=round(consumed_val - goal_val, 2) # (Score - Goal)
            )
        )
    
    # 5. Build the final response
    dashboard_response = schemas.DashboardResponse(
        log_date=log_date,
        matched_demographic_group=demographic_group.name,
        
        total_calories_goal=round(rda_goals.get("Energy", 0.0), 2),
        total_calories_consumed=round(total_consumption.get("Energy", 0.0), 2),
        total_protein_goal=round(rda_goals.get("Protein", 0.0), 2),
        total_protein_consumed=round(total_consumption.get("Protein", 0.0), 2),
        total_fat_goal=round(rda_goals.get("Visible Fat", 0.0), 2), # Using "Visible Fat" for goal
        total_fat_consumed=round(total_consumption.get("Fat", 0.0), 2), # Using total "Fat" for consumed
        total_carbs_goal=round(rda_goals.get("Carbohydrate", 0.0), 2),
        total_carbs_consumed=round(total_consumption.get("Carbohydrate", 0.0), 2),
        
        detailed_analysis=analysis_report
    )
    
    return dashboard_response

