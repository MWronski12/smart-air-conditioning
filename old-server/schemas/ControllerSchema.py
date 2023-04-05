from typing import Optional
from pydantic import Field
from schemas import DeviceSchema


class ControllerSchema(DeviceSchema):
    """
    duty: PWM duty cycle (0-100)
    fan: Fan off or on (0 or 1)
    mode: Fan mode cool or heat (0 or 1)
    """

    duty: Optional[int]
    fan: Optional[int]
    mode: Optional[int]
