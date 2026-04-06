from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    gender: str
    age: str
    phone: Optional[str] = None  # <-- optional field


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInfoDecode(BaseModel):
    jwttoken: str
