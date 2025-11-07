from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User, UserProfile
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/")
async def get_recommendations(  # Keep async here
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized weight loss recommendations"""
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    if not all([profile.birth_date, profile.gender, profile.height_cm, profile.weight_kg, profile.activity_level]):
        raise HTTPException(status_code=400, detail="Complete profile required for recommendations")
    
    profile_data = {
        'birth_date': profile.birth_date,
        'gender': profile.gender.value,
        'height_cm': profile.height_cm,
        'weight_kg': profile.weight_kg,
        'activity_level': profile.activity_level.value,
        'dietary_preference': profile.dietary_preference or 'mixed',
        'budget_range': profile.budget_range or 'medium',
        'preferred_cuisine': profile.preferred_cuisine or 'indian'
    }
    
    service = RecommendationService()
    recommendations = await service.generate_recommendations(profile_data)  # Now with await
    
    return recommendations