from typing import Optional
from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: str
    name: Optional[str]
