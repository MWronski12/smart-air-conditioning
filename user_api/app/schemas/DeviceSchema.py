from typing import Optional
from pydantic import BaseModel
from .RoomSchema import RoomSchema


class DeviceSchema(BaseModel):
    id: str
    name: Optional[str]
    room: Optional[str]
