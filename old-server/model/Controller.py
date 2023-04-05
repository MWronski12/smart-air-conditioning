from model import Device
from schemas import ControllerSchema


class Controller(Device):
    def __init__(self, room_id: int, device_id: int, fan_speed: int) -> None:
        super.__init__(self, room_id, device_id)
        self.fan_speed = fan_speed

    @classmethod
    def fromControllerSchema(cls, controllerSchema: ControllerSchema):
        return cls(
            controllerSchema.room_id,
            controllerSchema.devId,
            controllerSchema.fanSpeed,
        )
