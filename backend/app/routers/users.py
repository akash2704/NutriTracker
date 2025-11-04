from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # We can add a dependency to the *entire router*
    # but for clarity, we'll add it to the endpoint.
)

@router.get(
    "/me", 
    response_model=schemas.User
)
def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    """
    Fetches the profile for the *currently authenticated user*.
    
    The user is identified by the JWT token in the Authorization header.
    All the work is done by the `get_current_user` dependency.
    """
    # By the time this code runs, 'current_user' is already
    # the fully validated User model from the database.
    # We just have to return it.
    return current_user
