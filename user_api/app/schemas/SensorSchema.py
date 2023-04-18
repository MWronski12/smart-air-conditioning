from typing import Optional
from .DeviceSchema import DeviceSchema


class SensorSchema(DeviceSchema):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
