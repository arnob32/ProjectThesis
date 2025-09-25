from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str
    student_id: Optional[str] = None
    teacher_id: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  # allow ORM -> Pydantic conversion
