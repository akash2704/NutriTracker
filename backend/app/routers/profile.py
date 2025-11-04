from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services, models
from ..dependencies import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    # All endpoints in this router will require a valid token
    dependencies=[Depends(get_current_user)]
)

@router.post(
    "/me",
    response_model=schemas.Profile,
    summary="Create or Update User Profile"
)
def create_or_update_current_user_profile(
    profile_in: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create or update the profile for the currently authenticated user.
    
    This endpoint takes the user's physical stats (birth date, gender,
    activity level, height, weight) and:
    1. Calculates their age.
    2. Matches them to the correct NIN Demographic Group.
    3. Saves all this information to their profile.
    
    This is a required step before using the /dashboard endpoint.
    """
    return services.create_or_update_profile(
        db=db, 
        current_user=current_user, 
        profile_in=profile_in
    )

@router.get(
    "/me",
    response_model=schemas.Profile,
    summary="Get User Profile"
)
def get_current_user_profile(
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve the profile for the currently authenticated user.
    
    Will return a 404 error if the user has not created their
    profile yet.
    """
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please create your profile."
        )
    return current_user.profile

