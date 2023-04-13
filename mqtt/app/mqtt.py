import paho.mqtt.client as mqtt
import grpc

from .protos import influxdb_pb2, influxdb_pb2_grpc
from .config import *


class MqttClient:
    def __init__(self, username=None, password=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.username = username
        self.password = password

    def connect(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, message):
        # Topic format:
        # pbl6/<room_id>/<device_id>/sensor/<data_type>
        # data_type: humidity, temperature

        topic = message.topic.split("/")
        payload = message.payload.decode("utf-8")

        room_id = topic[1]
        device_id = topic[2]
        data_type = topic[4]

        channel = grpc.insecure_channel("localhost:50051")
        stub = influxdb_pb2_grpc.InfluxdbServiceStub(channel)
        stub.WriteMeasurement()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
