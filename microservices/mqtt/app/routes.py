from fastapi import APIRouter, HTTPException
from paho.mqtt import MQTTException
from model import Settings
from mqtt import MqttClient
from config import *

router = APIRouter()
mqtt_client = MqttClient(MQTT_HOST, MQTT_PORT)


@router.post("/devices/{room_id}/{device_id}/settings")
async def set_device_settings(room_id: str, device_id: str, settings: Settings):
    topic = f"application/{room_id}/{device_id}/setting/"
    payload = {"fan_speed": settings.fan_speed, "temperature": settings.temperature}
    try:
        mqtt_client.publish(topic, payload)
    except MQTTException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Settings updated successfully"}
