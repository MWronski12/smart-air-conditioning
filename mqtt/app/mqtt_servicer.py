import grpc

from .protos import mqtt_pb2, mqtt_pb2_grpc
from .mqtt import MqttClient
from .config import MQTT_HOST, MQTT_PORT


class MqttServicer(mqtt_pb2_grpc.MqttServiceServicer):
    def __init__(self):
        self.mqtt_client = MqttClient(MQTT_HOST, MQTT_PORT)

    def PublishDeviceSettings(self, request: mqtt_pb2.Settings, context):
        basetopic = (
            lambda data_type: f"pbl6/{request.room_id}/{request.device_id}/controller/{data_type}"
        )

        topic = basetopic("fan_speed")
        payload = str(request.fan_speed)
        self.mqtt_client.publish(topic, payload)

        topic = basetopic("temperature")
        payload = str(request.temperature)
        self.mqtt_client.publish(topic, payload)
