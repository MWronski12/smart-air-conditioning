# Imports

import influxdb_client
import uvicorn
from fastapi import FastAPI
from influxdb_client import InfluxDBClient, Point
import firebase_admin
from firebase_admin import credentials
import uuid
from uuid import UUID

from model import *
from private import *
from schemas import *
from schemas import UserSchema
from services import *

# Constants

MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883

# Globals

"""
    MQTT topic structure:
    pbl5/<room_id>/<device_id>/sensor: {temperature: float, humidity: float, ...}
                          |-> /controller: {fan_speed: int, cooling: bool, ...}
"""

app = FastAPI()
influxdb_client = InfluxDBClient(
    url=INFLUXDB_HOST,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG,
)
mqtt = Mqtt(MQTT_HOST, MQTT_PORT, influxdb_client)


# Functions


def mqtt_topic(room_id: str, device_id: int, dev_type: str, data_type: str) -> str:
    return f"pbl5/{room_id}/{device_id}/{dev_type}/{data_type}"


# Routes


@app.get("/api/v1")
def home():
    return "Hello World"


@app.get("/api/v1/rooms/{room_id}/devices/{device_id}/data")
def device_get(room_id: str, device_id: int) -> dict:

    query = f'from(bucket: "air-conditioning") \
    |> range(start: -6h) \
    |> filter(fn: (r) \
        => r._measurement == "sensor" \
        and r.device_id == "{device_id}" \
        and r.room_id == "{room_id}")'

    tables = influxdb_client.query_api().query(org=INFLUXDB_ORG, query=query)
    temperature_list = list()
    humidity_list = list()

    for table in tables:
        for record in table.records:
            data_type = record.get_field()
            timestamp = record.get_time()
            if data_type == "temperature":
                temperature_list.append(
                    timestamp=timestamp,
                    temperature=record.get_value(),
                )
            elif data_type == "humidity":
                humidity_list.append(
                    HumiditySchema(
                        timestamp=timestamp,
                        humidity=record.get_value(),
                    )
                )
    return {"temperature": temperature_list, "humidity": humidity_list}


@app.get("/api/v1/rooms/{room_id}/devices")
def devices_get(room_id: str) -> list:
    ret = FirebaseRTDB.get(f"rooms/{room_id}/devices")
    if ret is None:
        return []
    else:
        return [DeviceSchema(**val) for val in ret.values()]


@app.post("/api/v1/rooms/{room_id}/devices/register")
def device_post(room_id: str, device: DeviceSchema) -> DeviceSchema:
    FirebaseRTDB.add(f"rooms/{room_id}/devices/{device.devId}", device.dict())
    return device


@app.post("/api/v1/rooms/{room_id}/devices/{device_id}/command")
def command_post(room_id: str, device_id: int, controller: ControllerSchema):
    for key, value in controller.dict(exclude_none=True).items():
        if key in ["fan", "duty", "mode"]:
            mqtt.publish(mqtt_topic(room_id, device_id, "controller", key), value)
    return controller


@app.get("/api/v1/rooms")
def rooms_get():
    ret = FirebaseRTDB.get("rooms")
    if ret is None:
        return []
    else:
        return [RoomSchema(uuid=val["uuid"], name=val["name"]) for val in ret.values()]


@app.post("/api/v1/rooms")
def rooms_post(room: str) -> RoomSchema:
    roomId = uuid.uuid4().hex
    FirebaseRTDB.add(f"rooms/{roomId}", RoomSchema(uuid=roomId, name=room).dict())
    return RoomSchema(uuid=roomId, name=room)


@app.post("/api/v1/users")
def users_post(user: UserSchema) -> UserSchema:
    FirebaseRTDB.add(f"users/{user.uid}", user.dict())
    return user


@app.get("/api/v1/users/{uid}")
def users_get(uid: str) -> UserSchema:
    ret = FirebaseRTDB.get(f"users/{uid}")
    if ret is None:
        return None
    else:
        return UserSchema(**ret)


@app.put("/api/v1/users/{uid}")
def users_put(uid: str, user: UserSchema) -> UserSchema:
    FirebaseRTDB.update(f"users/{uid}", user.dict())
    return user


@app.post("/api/v1/users/{uid}/rooms/{room_id}/devices/{device_id}")
def users_preference_post(
    uid: str, room_id: str, device_id: int, controller: ControllerSchema
):
    FirebaseRTDB.add(
        f"users/{uid}/rooms/{room_id}/devices/{device_id}", controller.dict()
    )
    return controller


# Main

if __name__ == "__main__":
    firebaseCred = credentials.Certificate("pbl5-firebase-admin-key.json")
    firebase_admin.initialize_app(
        firebaseCred,
        {
            "databaseURL": "https://pbl5-5d9d2-default-rtdb.europe-west1.firebasedatabase.app/"
        },
    )
    mqtt.start()
    mqtt.client.loop_start()
    mqtt.subscribe("pbl5/#")
    uvicorn.run(app, host="192.168.8.106", port=8000)
