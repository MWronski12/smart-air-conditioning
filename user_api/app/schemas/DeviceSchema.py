from typing import Optional
from pydantic import BaseModel
from .RoomSchema import RoomSchema


class DeviceSchema(BaseModel):
    id: int
    name: Optional[str]
    room: Optional[RoomSchema]
