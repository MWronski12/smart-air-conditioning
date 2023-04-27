from fastapi import APIRouter, HTTPException, status
import grpc
import uuid
from .protos import (
    database_pb2,
    database_pb2_grpc,
    influxdb_pb2,
    influxdb_pb2_grpc,
    mqtt_pb2,
    mqtt_pb2_grpc,
)
from .schemas import *

BASE_URL = "/api/v1"

router = APIRouter(prefix=BASE_URL)

database_channel = grpc.insecure_channel("database_service:50051")
influxdb_channel = grpc.insecure_channel("influxdb_service:50051")
mqtt_channel = grpc.insecure_channel("mqtt_service:50051")

database_stub = database_pb2_grpc.DatabaseServiceStub(database_channel)
influxdb_stub = influxdb_pb2_grpc.InfluxdbServiceStub(influxdb_channel)
mqtt_stub = mqtt_pb2_grpc.MqttServiceStub(mqtt_channel)


# ------------ Interfacing with InfluxDB ------------#


@router.get("/rooms/{room_id}/devices/{device_id}/data")
def get_device_data(room_id: str, device_id: int):
    pass
    # request = influxdb_pb2.ReadMeasurementsRequest(
    #     room_id=room_id, device_id=device_id, has_humidity=True, has_temperature=True
    # )

    # channel = grpc.insecure_channel("influxdb:8086")
    # with InfluxdbServiceStub(channel) as stub:
    #     pass

    # tables = influxdb_client.query_api().query(org=INFLUXDB_ORG, query=query)
    # temperature_list = list()
    # humidity_list = list()

    # for table in tables:
    #     for record in table.records:
    #         data_type = record.get_field()
    #         timestamp = record.get_time()
    #         if data_type == "temperature":
    #             temperature_list.append(
    #                 record.get_value(),
    #             )
    #         elif data_type == "humidity":
    #             humidity_list.append(
    #                 record.get_value(),
    #             )
    # return {"temperature": temperature_list, "humidity": humidity_list}


# ------------ Interfacing with the database ------------#


@router.get("/rooms")
def get_all_rooms() -> list:
    try:
        response: database_pb2.GetAllRoomsResponse = database_stub.GetAllRooms(
            database_pb2.GetAllRoomsRequest(),
        )
        room_list = [{"id": room.id, "name": room.name} for room in response.rooms]
        return room_list
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.details(),
            )


@router.post("/rooms")
def post_room(room: str) -> RoomSchema:
    roomId = uuid.uuid4().hex
    try:
        response: database_pb2.AddRoomResponse = database_stub.AddRoom(
            database_pb2.AddRoomRequest(
                room=database_pb2.Room(
                    id=roomId,
                    name=room,
                )
            )
        )
        return RoomSchema(id=response.room.id, name=response.room.name)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=e.details()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.details()
            )


@router.get("/rooms/{room_id}/devices")
def get_devices_in_room(room_id: str) -> list:
    try:
        response: database_pb2.GetDevicesInRoomResponse = (
            database_stub.GetDevicesInRoom(
                database_pb2.GetDevicesInRoomRequest(room_id=room_id)
            )
        )
        devices = [
            {"id": device.id, "name": device.name, "room": room_id}
            for device in response.devices
        ]
        print(device)
        return devices
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.details()
            )


@router.post("/rooms/{room_id}/devices/register")
def register_device(room_id: str, device: DeviceSchema) -> DeviceSchema:
    try:
        response: database_pb2.AddDeviceResponse = database_stub.AddDevice(
            database_pb2.AddDeviceRequest(
                room_id=room_id,
                device=database_pb2.Device(
                    id=device.id,
                    name=device.name,
                ),
            )
        )
        return DeviceSchema(
            id=response.device.id, name=response.device.name, room=room_id
        )
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.details(),
            )
        elif e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.details(),
            )


@router.post("/users")
def post_user(user: UserSchema) -> UserSchema:
    try:
        database_stub.AddUser(
            database_pb2.AddUserRequest(
                user=database_pb2.User(
                    id=user.id,
                    name=user.email,
                )
            )
        )
        return user
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@router.get("/users/{uid}")
def get_user(uid: str) -> UserSchema:
    try:
        response: database_pb2.GetUserResponse = database_stub.GetUser(
            database_pb2.GetUserRequest(
                id=uid,
            )
        )
        return UserSchema(id=response.user.id, email=response.user.name)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@router.post("/users/{uid}/preferences")
def post_user_preference(uid: str, preference: PreferenceSchema) -> PreferenceSchema:
    try:
        database_stub.SetUserPreferences(
            database_pb2.SetUserPreferencesRequest(
                user_id=uid,
                preferences=database_pb2.Preference(
                    temperature=preference.temperature,
                    fan_speed=preference.fan_speed,
                    room_id=preference.room_id,
                ),
            )
        )
        return preference
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.details(),
            )


@router.get("/users/{uid}/preferences/{room_id}")
def get_user_preference(uid: str, room_id: str):
    pass

# ------------ Interfacing with MQTT ------------#


@router.post("/rooms/{room_id}/devices/{device_id}/command")
def post_command(room_id: str, device_id: str, controller: ControllerSchema):
    try:
        response = mqtt_stub.PublishDeviceSettings(
            mqtt_pb2.PublishDeviceSettingsRequest(
                mqtt_pb2.Settings(
                    room_id=room_id,
                    device_id=device_id,
                    temperature=controller.temperature,
                    fan_speed=controller.fan_speed,
                )
            )
        )
        return response
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
