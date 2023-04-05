from model import Sensor
from schemas import SensorSchema


class DeviceRepository:
    devices = set()

    @staticmethod
    def get(device_id) -> Sensor:
        sensor: Sensor = next((sensor for sensor in DeviceRepository.devices if sensor.device_id == device_id), None)
        return sensor.getSensorSchema()

    @staticmethod
    def add(sensorSchema: SensorSchema) -> SensorSchema:
        DeviceRepository.devices.add(Sensor.fromSensorSchema(sensorSchema))
        return sensorSchema
