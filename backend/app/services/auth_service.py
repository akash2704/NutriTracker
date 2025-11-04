from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from ..security import hash_password, create_otp, verify_password # <-- Add verify_password
from datetime import datetime, timedelta, timezone
from .email import email_service

# --- NEW FUNCTION ---
def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Fetches a single user by their email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

# --- NEW FUNCTION ---
def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    """
    Handles the core login logic:
    1. Find user by email.
    2. Check if account is active.
    3. Verify the password.
    Returns the User model if successful, else None.
    """
    user = get_user_by_email(db, email)
    
    if not user:
        # User not found
        return None
        
    if not user.is_active:
        # User found but account not verified
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Please check your email for an OTP."
        )

    if not verify_password(password, user.hashed_password):
        # Password was incorrect
        return None
    
    # All checks passed!
    return user

def create_user(db: Session, user: schemas.UserCreate):
    """
    Business logic for creating a new user.
    Now creates an INACTIVE user with an OTP.
    """
    # 1. Check if user with this email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user and existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered and active."
        )
    
    # 2. Hash the plain-text password
    hashed_pw = hash_password(user.password)
    
    # 3. Generate OTP and expiry
    otp = create_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15) # 15 min expiry
    
    # 4. Create or Update the User model
    if existing_user:
        # User exists but is not active, update their password and OTP
        existing_user.hashed_password = hashed_pw
        existing_user.first_name = user.first_name
        existing_user.last_name = user.last_name
        existing_user.verification_otp = otp
        existing_user.otp_expires_at = expires_at
        db_user = existing_user
    else:
        # Create a new user
        user_data = user.model_dump(exclude={'password'})
        db_user = models.User(
            **user_data,
            hashed_password=hashed_pw,
            verification_otp=otp,
            otp_expires_at=expires_at,
            is_active=False # Default is False, but being explicit
        )
        db.add(db_user)

    db.commit()
    db.refresh(db_user)
    
    # Send OTP via email
    email_sent = email_service.send_otp_email(db_user.email, otp, db_user.first_name)
    
    # Return OTP only if email wasn't sent (development mode)
    return {"user": db_user, "otp": None if email_sent else otp}

def verify_user_otp(db: Session, verification: schemas.UserVerify):
    """
    Business logic for verifying a user's OTP.
    """
    user = db.query(models.User).filter(models.User.email == verification.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already active.")

    # --- FIX FOR DATETIME COMPARISON ---
    # Ensure both datetimes are timezone-aware (UTC) before comparing
    
    # Get the current time as timezone-aware (UTC)
    current_time_utc = datetime.now(timezone.utc)
    
    # Get the expiry time from the database
    expiry_time_from_db = user.otp_expires_at

    # Check if the expiry time retrieved from the DB is naive
    if expiry_time_from_db.tzinfo is None:
        # If it's naive, assume it represents UTC and make it aware
        expiry_time_utc = expiry_time_from_db.replace(tzinfo=timezone.utc)
    else:
        # If it's already aware (e.g., DB stores with timezone), use it directly
        expiry_time_utc = expiry_time_from_db
        
    # Now compare the two aware datetime objects
    if expiry_time_utc < current_time_utc:
    # --- END OF FIX ---
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired.")
        
    if user.verification_otp != verification.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")

    # All checks passed! Activate the user.
    user.is_active = True
    user.verification_otp = None
    user.otp_expires_at = None
    
    db.commit()
    db.refresh(user)
    return user