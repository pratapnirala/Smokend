from pydantic import BaseModel, EmailStr


class Challange(BaseModel):
    insomnia: bool
    infoxin: bool
    craving: bool
    extraInfo: str



