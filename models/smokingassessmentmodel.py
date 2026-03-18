from pydantic import BaseModel, EmailStr


class Assessment(BaseModel):
    cigarettesPerDay: int
    motivation: int
    quitAttempts: int
    yearsSmoking: int
    userID: str



