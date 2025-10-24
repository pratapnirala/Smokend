from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    gender: str
    age: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInfoDecode(BaseModel):
    jwttoken: str
