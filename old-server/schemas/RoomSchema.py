from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class RoomSchema(BaseModel):
    uuid: str
    name: Optional[str]
    