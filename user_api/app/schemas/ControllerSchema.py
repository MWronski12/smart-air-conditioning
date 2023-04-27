from typing import Optional
from pydantic import Field
from .DeviceSchema import DeviceSchema


class ControllerSchema(DeviceSchema):
    fan_speed: Optional[int]
    temperature: Optional[int]
