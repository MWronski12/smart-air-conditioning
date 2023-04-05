import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class Mqtt:
    def __init__(self, host: str, port: int, influx_client: InfluxDBClient):
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")

        def on_message(client, userdata, msg):
            # topic pbl5/<room_id>/<device_id>/sensor/<data_type>
            topic = msg.topic.split("/")
            room_id = str(topic[1])
            device_id = str(topic[2])
            dev_type = topic[3]
            data_type = topic[4]
            data = msg.payload.decode("utf-8")
            print(
                f"Received message from {room_id}/{device_id} of type {dev_type}: {data} and data type: {data_type}"
            )
            if dev_type == "sensor":
                point = (
                    Point("sensor")
                    .tag("room_id", room_id)
                    .tag("device_id", device_id)
                    .field(data_type, data)
                )
                self.influx_client.write_api().write(
                    bucket="air-conditioning", write_options=SYNCHRONOUS, record=point
                )

        def on_disconnect(client, userdata, rc):
            print(f"Disconnected with result code {rc}")

        def on_publish(client, userdata, rc):
            print(f"Published with result code {rc}")

        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        self.client.on_publish = on_publish
        self.influx_client = influx_client

    def start(self):
        print(f"Starting MQTT client on {self.host}:{self.port}")
        self.client.connect(self.host, self.port)

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def publish(self, topic, payload, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain)
