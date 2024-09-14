"""Common schemad for request"""

from pydantic import BaseModel, EmailStr, Field
from app.core.constant import UserRole

# Schema for request validation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole = UserRole.user


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    userId: int
    username: str
    userRole: UserRole

class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

class SubServiceCreate(BaseModel):
    service_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)