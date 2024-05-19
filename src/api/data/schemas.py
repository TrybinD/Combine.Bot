from pydantic import BaseModel

class Event(BaseModel):
    name: str
    token: str
    description: str

