from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import schemas, models, services
from ..database import get_db
from ..dependencies import get_current_user # <-- Our "Security Guard"

# Create a new router
router = APIRouter(
    prefix="/food-logs",
    tags=["Logs"],
    # We can add dependencies to the entire router,
    # but for clarity, we'll add it to each endpoint.
)

@router.post(
    "/", 
    response_model=schemas.Log, 
    status_code=status.HTTP_201_CREATED
)
def create_log(
    log_in: schemas.LogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Creates a new food log entry for the *currently authenticated user*.
    
    The user is identified by their JWT token.
    The log data is sent in the request body.
    """
    # The 'current_user' is our fully validated User model from the dependency.
    # We pass their ID to the service layer to create the link.
    return services.create_log_entry(
        db=db, 
        log_in=log_in, 
        user_id=current_user.id
    )

@router.get("/", response_model=List[schemas.FoodLogResponse])
def get_food_logs(
    log_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get food logs for a specific date or today"""
    return services.get_food_logs(db=db, user_id=current_user.id, log_date=log_date)