from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """ Base user schema (shared properties). """
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    """ Schema for *creating* a user (i.e., registration). """
    password: str 
class User(UserBase):
    """ Schema for *reading* a user (what we return from the API). """
    id: int
    is_active: bool 
    
    class Config:
        from_attributes = True



class UserRegisterResponse(BaseModel):
    """
    What we return after registration.
    In a real app, we would NOT send the OTP.
    Here we do it to simulate the user receiving it.
    """
    user: User
    otp: Optional[str] = None

class UserVerify(BaseModel):
    """
    The schema the user sends to the /verify endpoint.
    """
    email: EmailStr
    otp: str

class Token(BaseModel):
    """
    The response model we send back to the user after login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    The data we store *inside* the JWT (the payload).
    """
    email: Optional[str] = None
