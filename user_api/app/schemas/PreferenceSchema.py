from typing import Optional
from pydantic import BaseModel


class PreferenceSchema(BaseModel):
    fan_speed: Optional[int]
    temperature: Optional[float]
