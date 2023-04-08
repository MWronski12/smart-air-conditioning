import grpc
import mqtt_pb2
import mqtt_pb2_grpc

from .mqtt import MqttClient
from .config import MQTT_HOST, MQTT_PORT

mqtt_client = MqttClient(MQTT_HOST, MQTT_PORT)


class MqttServicer(mqtt_pb2_grpc.MqttServiceServicer):
    def __init__(self):
        pass

    def PublishDeviceSettings(self, request: mqtt_pb2.Settings, context):
        topic = f"application/{request.room_id}/{request.device_id}/command"
        payload = {"fan_speed": {request.fan_speed}, "temperature": {request.temperature}}
        mqtt_client.publish(topic, payload)
