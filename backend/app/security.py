import bcrypt
import secrets
import string
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from . import schemas # We'll need this for the token payload
from dotenv import load_dotenv
load_dotenv()
# --- LOAD FROM .ENV ---
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])


def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    # Generate a "salt" to make the hash unique
    salt = bcrypt.gensalt()
    # Hash the password (must be encoded to bytes)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hash as a string
    return hashed_pw.decode('utf-8')

def create_otp(length: int = 6) -> str:
    """Generates a secure random OTP."""
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

# --- NEW FUNCTION ---
def create_access_token(data: dict) -> str:
    """
    Generates a new JWT access token.
    """
    to_encode = data.copy()
    
    # Add an expiry time
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_at})
    
    # Create the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt