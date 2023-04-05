from uuid import UUID
from model import Device
from schemas import SensorSchema


class Sensor(Device):
    def __init__(
        self, room_id: UUID, device_id: int, temperature: float, humidity: float
    ) -> None:
        super().__init__(room_id, device_id)
        self.temperature = temperature
        self.humidity = humidity

    @classmethod
    def fromSensorSchema(cls, sensorSchema: SensorSchema):
        return cls(
            sensorSchema.room_id,
            sensorSchema.devId,
            sensorSchema.temperature,
            sensorSchema.humidity,
        )

    def getSensorSchema(self) -> SensorSchema:
        return SensorSchema(
            room_id=self.room_id,
            devId=self.device_id,
            temperature=self.temperature,
            humidity=self.humidity,
        )

    def __hash__(self) -> int:
        return super().__hash__()
