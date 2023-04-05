from pydantic import BaseModel

class UserSchema(BaseModel):
    uid: str
    email: str
    isPresent: bool
