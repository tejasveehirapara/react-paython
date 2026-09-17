from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(UserCreate):
    pass


class LoginData(BaseModel):
    session_id: int
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
