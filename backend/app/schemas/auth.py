from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = "ADMIN"

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str
    is_active: int

    class Config:
        from_attributes = True
