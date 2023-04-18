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
from schemas import *

BASE_URL = "/api/v1"

router = APIRouter(prefix=BASE_URL)

database_channel = grpc.insecure_channel("database:50051")
influxdb_channel = grpc.insecure_channel("influxdb:50051")
mqtt_channel = grpc.insecure_channel("mqtt:50051")

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
def rooms_get() -> list:
    try:
        response = database_stub.GetAllRooms()
        return response.rooms
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No rooms found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@router.post("/rooms")
def rooms_post(room: str) -> RoomSchema:
    roomId = uuid.uuid4().hex
    try:
        response = database_stub.AddRoom(
            database_pb2.AddRoomRequest(database_pb2.Room(id=roomId, name=room))
        )
        return RoomSchema(id=response.id, name=response.name)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@router.get("/rooms/{room_id}/devices")
def get_devices_in_room(room_id: str) -> list:
    try:
        response = database_stub.GetDevicesInRoom(
            database_pb2.GetDevicesInRoomRequest(room_id=room_id)
        )
        return response.devices
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No devices found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


@router.post("/rooms/{room_id}/devices/register")
def device_post(room_id: str, device: DeviceSchema) -> DeviceSchema:
    FirebaseRTDB.add(f"rooms/{room_id}/devices/{device.devId}", device.dict())
    return device


@router.post("/rooms/{room_id}/devices/{device_id}/command")
def command_post(room_id: str, device_id: int, controller: ControllerSchema):
    for key, value in controller.dict(exclude_none=True).items():
        if key in ["fan", "duty", "mode"]:
            mqtt.publish(mqtt_topic(room_id, device_id, "controller", key), value)
    return controller


@router.post("/users")
def users_post(user: UserSchema) -> UserSchema:
    FirebaseRTDB.add(f"users/{user.uid}", user.dict())
    return user


@router.get("/users/{uid}")
def users_get(uid: str) -> UserSchema:
    ret = FirebaseRTDB.get(f"users/{uid}")
    if ret is None:
        return None
    else:
        return UserSchema(**ret)


@router.put("/users/{uid}")
def users_put(uid: str, user: UserSchema) -> UserSchema:
    FirebaseRTDB.update(f"users/{uid}", user.dict())
    return user


@router.post("/users/{uid}/rooms/{room_id}/devices/{device_id}")
def users_preference_post(
    uid: str, room_id: str, device_id: int, controller: ControllerSchema
):
    FirebaseRTDB.add(
        f"users/{uid}/rooms/{room_id}/devices/{device_id}", controller.dict()
    )
    return controller


@router.get("/users/{uid}/rooms/{room_id}/devices/{device_id}")
def users_preference_get(uid: str, room_id: str, device_id: int):
    ret = FirebaseRTDB.get(f"users/{uid}/rooms/{room_id}/devices/{device_id}/duty")
    print(f"{ret}")
    return ret
