from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import ValidationError  # <-- THIS IS THE FIX
from . import schemas, services, models
from .database import get_db
from .security import SECRET_KEY, ALGORITHM

# This is the "Guard's Hand".
# It's an object that knows how to find the "Bearer" token.
# The `tokenUrl` tells the /docs page which endpoint to use to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.User:
    """
    This is the "Security Guard" dependency.
    It will be run on every protected endpoint.
    
    1. Gets the token from the Authorization header (via oauth2_scheme).
    2. Gets a DB session (via get_db).
    3. Decodes the token.
    4. Fetches the user from the DB.
    5. Returns the user model, or raises an error.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 3. Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 4. Extract the email (which we stored in the 'sub' field)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        # 5. Validate the data with our schema
        token_data = schemas.TokenData(email=email)
        
    except (JWTError, ValidationError): # <-- FIXED (was schemas.ValidationError)
        # Catches bad signatures, expired tokens, or bad data
        raise credentials_exception
        
    # 6. Fetch the user from the DB
    user = services.get_user_by_email(db, email=token_data.email)
    
    if user is None:
        # If user was deleted after token was issued
        raise credentials_exception
        
    if not user.is_active:
        # If user was deactivated
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    # 7. Return the full User model
    return user

