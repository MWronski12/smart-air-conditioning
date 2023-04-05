from typing import Optional
from schemas import DeviceSchema


class SensorSchema(DeviceSchema):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
