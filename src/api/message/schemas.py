from pydantic import BaseModel

class SendRequest(BaseModel):
    user_id: int
    message: str

