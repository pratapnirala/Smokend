from pydantic import BaseModel, EmailStr



class Assessment(BaseModel):
    cigarettesPerDay: int
    motivation: int
    quitAttempts: int
    yearsSmoking: int
    costPerPack: float
    userID: str
