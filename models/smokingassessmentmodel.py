from pydantic import BaseModel, EmailStr
from decimal import Decimal


class Assessment(BaseModel):
    cigarettesPerDay: int
    motivation: int
    quitAttempts: int
    yearsSmoking: int
    costPerPack: Decimal
    userID: str
