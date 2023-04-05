from typing import Optional
from pydantic import BaseModel

from schemas import RoomSchema


class DeviceSchema(BaseModel):
    devId: int
    name: Optional[str]
    room: Optional[RoomSchema]