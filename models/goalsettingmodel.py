from pydantic import BaseModel


class smokgoleset(BaseModel):
    custom_reason: str
    main_reason: str
    userID: str
