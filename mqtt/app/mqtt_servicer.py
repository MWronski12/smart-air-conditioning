import grpc
import logging

from .protos import mqtt_pb2, mqtt_pb2_grpc
from .mqtt import MqttClient
from .config import MQTT_HOST, MQTT_PORT


class MqttServicer(mqtt_pb2_grpc.MqttServiceServicer):
    def __init__(self):
        self.mqtt_client = MqttClient(MQTT_HOST, MQTT_PORT)

    def add_to_server(self, server: grpc.Server):
        mqtt_pb2_grpc.add_MqttServiceServicer_to_server(self, server)

    def PublishDeviceSettings(self, request: mqtt_pb2.PublishDeviceSettingsRequest, context):
        for data_type in ["fan_speed", "temperature"]:
            topic = f"pbl6/{request.settings.room_id}/{request.settings.device_id}/controller/{data_type}"
            payload = getattr(request.settings, data_type)
            self.mqtt_client.publish(topic, payload)

        return mqtt_pb2.PublishDeviceSettingsResponse(message="ok")
