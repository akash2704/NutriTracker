from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services
from ..database import get_db
from ..security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm 
router = APIRouter(
    prefix="/auth",  # All routes in this file will start with /auth
    tags=["Authentication"]
)
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Handles user login and returns a JWT access token.
    
    This uses an OAuth2-compatible form body:
    - username: The user's email
    - password: The user's plain-text password
    """
    # 1. Authenticate the user (service layer)
    #    We use form_data.username as the email
    user = services.authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        # This is a generic error for security
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header
        )
    
    # 2. Create the JWT
    #    We store the user's email in the 'sub' (subject) field
    token_data = {"sub": user.email}
    access_token = create_access_token(data=token_data)
    
    # 3. Return the token
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    "/register", 
    response_model=schemas.UserRegisterResponse, # <-- CHANGED response model
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate, # This is the Request Body
    db: Session = Depends(get_db)
):
    """
    Register a new user (inactive).
    
    Creates a new user with `is_active=False` and generates an OTP.
    In a real app, this would email the OTP.
    For this simulation, the OTP is returned in the response.
    """
    # Pass all the data to the service layer to do the work
    return services.create_user(db=db, user=user)

@router.post(
    "/verify",
    response_model=schemas.User
)
def verify_user(
    verification_data: schemas.UserVerify, # <-- NEW Request Body
    db: Session = Depends(get_db)
):
    """
    Verify a new user's account using an OTP.
    
    Takes the user's email and the OTP.
    If valid and not expired, sets the user's `is_active` flag to True.
    """
    return services.verify_user_otp(db=db, verification=verification_data)
