import paho.mqtt.client as mqtt
import grpc
import logging

from .protos import influxdb_pb2, influxdb_pb2_grpc
from .config import *


class MqttClient:
    def __init__(self, username=None, password=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.username = username
        self.password = password
        self.connect()

    def connect(self):
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Connected to {MQTT_HOST}:{MQTT_PORT} with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.info(f"Disconnected from {MQTT_HOST}:{MQTT_PORT} with result code {rc}")

    def on_message(self, client, userdata, message):
        # Topic format:
        # pbl6/<room_id>/<device_id>/sensor/<data_type>
        # data_type: humidity, temperature

        topic = message.topic.split("/")
        payload = message.payload.decode("utf-8")

        room_id = topic[1]
        device_id = topic[2]
        data_type = topic[4]

        logging.info(f"Received message from {room_id}/{device_id}/{data_type}: {payload}")

        channel = grpc.insecure_channel("influxdb_service:50051")
        stub = influxdb_pb2_grpc.InfluxdbServiceStub(channel)
        stub.WriteMeasurement()

    def on_publish(self, client, userdata, mid):
        logging.info(f"Message {mid} published")

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
