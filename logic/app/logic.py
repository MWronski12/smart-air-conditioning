from typing import Dict
from .protos import database_pb2, database_pb2_grpc, mqtt_pb2, mqtt_pb2_grpc
import grpc
import logging


database_channel = grpc.insecure_channel("database_service:50051")
database_stub = database_pb2_grpc.DatabaseServiceStub(database_channel)

mqtt_channel = grpc.insecure_channel("mqtt_service:50051")
mqtt_stub = mqtt_pb2_grpc.MqttServiceStub(mqtt_channel)


def update_room_preferences(room_id):
    users = get_users_in_room(room_id=room_id).users
    preferences = get_average_preferences(users)

    logging.info(f"Updating room {room_id} preferences to {preferences}")

    devices = get_devices_in_room(room_id=room_id).devices
    for device in devices:
        settings = mqtt_pb2.Settings(
            room_id=room_id,
            device_id=device.id,
            temperature=preferences['avg_temp'],
            fan_speed=int(preferences['avg_fan_speed']),
        )
        mqtt_request = mqtt_pb2.PublishDeviceSettingsRequest(settings)
        mqtt_stub.PublishDeviceSettings(mqtt_request)


def get_user_room(user_id) -> database_pb2.GetUserRoomResponse:
    request = database_pb2.GetUserRoomRequest(user_id)
    return database_stub.GetUserRoom(request)


def set_device_settings(settings: mqtt_pb2.Settings) -> mqtt_pb2.PublishDeviceSettingsResponse:
    request = mqtt_pb2.PublishDeviceSettingsRequest(settings)
    return mqtt_stub.PublishDeviceSettings(request)


def get_users_in_room(room_id) -> database_pb2.GetUsersInRoomResponse:
    request = database_pb2.GetUsersInRoomRequest(
        room_id=room_id)
    return database_stub.GetUsersInRoom(request)


def get_devices_in_room(room_id) -> database_pb2.GetDevicesInRoomResponse:
    request = database_pb2.GetDevicesInRoomRequest(
        room_id=room_id)
    return database_stub.GetDevicesInRoom(request)


def get_average_preferences(users) -> Dict[str, float]:
    avg_temp = 0
    avg_fan_speed = 0
    user_with_preferences_count = 0

    for user in users:
        if user.preferences != None:
            avg_temp += user.preferences.temperature
            avg_fan_speed += user.preferences.fan_speed
            user_with_preferences_count += 1

    return {'avg_temp': avg_temp, 'avg_fan_speed': avg_fan_speed}
