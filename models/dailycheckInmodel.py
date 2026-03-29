from pydantic import BaseModel, EmailStr


class DailyCheckIn(BaseModel):
    mood: str
    motivation: int
    reason: str
    #userID: str



