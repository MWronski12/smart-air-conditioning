from pydantic import BaseModel

class UserSchema(BaseModel):
    id: str
    email: str
    isPresent: bool
