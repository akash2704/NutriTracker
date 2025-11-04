from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timezone

from .. import schemas, models, services
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)] # Protect ALL routes in this file
)

@router.get(
    "/", 
    response_model=schemas.DashboardResponse
)
def get_dashboard_report(
    # The user can specify a date, or it defaults to *today*
    log_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Provides a full nutritional gap analysis for the logged-in user
    for a specific date.
    
    If no date is provided, it defaults to the current date.
    """
    if log_date is None:
        log_date = datetime.now(timezone.utc).date()
        
    return services.get_dashboard_data(db=db, user=current_user, log_date=log_date)

