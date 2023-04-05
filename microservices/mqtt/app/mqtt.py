import paho.mqtt.client as mqtt
import requests

from config import *


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
        # Parse topic and payload
        topic_parts = message.topic.split("/")
        room_id = topic_parts[1]
        device_id = topic_parts[2]
        data_type = topic_parts[4]
        data_value = message.payload.decode()

        # Send request to InfluxDB microservice
        url = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}/write"
        data = f"sensor_data,room_id={room_id},device_id={device_id},data_type={data_type} value={data_value}"
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Data saved to InfluxDB")
        else:
            print(f"Failed to save data to InfluxDB: {response.text}")

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
