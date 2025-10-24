from pydantic import BaseModel



# ASK Request model
class Question(BaseModel):
    query: str
