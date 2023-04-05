from pydantic import BaseModel


class Settings(BaseModel):
    temperature: float
    fan_speed: int
