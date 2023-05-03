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


def grpc_call(stub, request, success_callback: callable):
    try:
        response = stub(request)
        return success_callback(response)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        elif e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.details(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.details(),
            )


# ------------ Interfacing with InfluxDB ------------#


@router.get("/rooms/{room_id}/devices/{device_id}/data")
def get_device_data(room_id: str, device_id: int):
    def success_callback(response: influxdb_pb2.ReadMeasurementsResponse):
        return {
            "temperature": [record.temperature for record in response.measurements],
            "humidity": [record.humidity for record in response.measurements],
        }

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
    def success_callback(response: database_pb2.GetAllRoomsResponse):
        return [{"id": room.id, "name": room.name} for room in response.rooms]

    return grpc_call(
        stub=database_stub,
        request=database_pb2.GetAllRoomsRequest(),
        success_callback=success_callback,
    )


@router.post("/rooms", status_code=status.HTTP_201_CREATED)
def add_room(room: str) -> RoomSchema:
    def success_callback(response: database_pb2.AddRoomResponse):
        return RoomSchema(id=response.room.id, name=response.room.name)

    return grpc_call(
        stub=database_stub,
        request=database_pb2.AddRoomRequest(
            room=database_pb2.Room(
                id=uuid.uuid4().hex,
                name=room,
            )
        ),
        success_callback=success_callback,
    )


@router.get("/rooms/{room_id}/devices")
def get_devices_in_room(room_id: str) -> list:
    def success_callback(response: database_pb2.GetDevicesInRoomResponse):
        return [
            {"id": device.id, "name": device.name, "room": room_id} for device in response.devices
        ]

    return grpc_call(
        stub=database_stub,
        request=database_pb2.GetDevicesInRoomRequest(room_id=room_id),
        success_callback=success_callback,
    )


@router.post("/rooms/{room_id}/devices", status_code=status.HTTP_201_CREATED)
def register_device(room_id: str, device: DeviceSchema) -> DeviceSchema:
    def success_callback(response: database_pb2.AddDeviceResponse):
        return DeviceSchema(id=response.device.id, name=response.device.name, room=room_id)

    return grpc_call(
        stub=database_stub,
        request=database_pb2.AddDeviceRequest(
            room_id=room_id,
            device=database_pb2.Device(
                id=device.id,
                name=device.name,
            ),
        ),
        success_callback=success_callback,
    )


@router.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(user: UserSchema) -> UserSchema:
    def success_callback(response: database_pb2.AddUserResponse):
        return UserSchema(id=response.user.id, email=response.user.email)

    return grpc_call(
        stub=database_stub,
        request=database_pb2.AddUserRequest(
            user=database_pb2.User(
                id=user.id,
                name=user.email,
            )
        ),
        success_callback=success_callback,
    )


@router.get("/users/{uid}")
def get_user(uid: str) -> UserSchema:
    def success_callback(response: database_pb2.GetUserResponse):
        return UserSchema(id=response.user.id, email=response.user.email)

    return grpc_call(
        stub=database_stub,
        request=database_pb2.GetUserRequest(
            id=uid,
        ),
        success_callback=success_callback,
    )


@router.post("/users/{uid}/preferences", status_code=status.HTTP_201_CREATED)
def post_user_preference(uid: str, preference: PreferenceSchema) -> PreferenceSchema:
    def success_callback(response: database_pb2.SetUserPreferencesResponse):
        return PreferenceSchema(
            temperature=response.preferences.temperature,
            fan_speed=response.preferences.fan_speed,
            room_id=response.preferences.room_id,
        )

    return grpc_call(
        stub=database_stub,
        request=database_pb2.SetUserPreferencesRequest(
            user_id=uid,
            preferences=database_pb2.Preference(
                temperature=preference.temperature,
                fan_speed=preference.fan_speed,
                room_id=preference.room_id,
            ),
        ),
        success_callback=success_callback,
    )


@router.post("/rooms/{room_id}/users", status_code=status.HTTP_201_CREATED)
def add_user_to_room(room_id: str, user_id: str) -> str:
    def success_callback(response: database_pb2.AddUserToRoomResponse):
        return response.user_id

    return grpc_call(
        stub=database_stub,
        request=database_pb2.AddUserToRoomRequest(
            room_id=room_id,
            user_id=user_id,
        ),
        success_callback=success_callback,
    )


@router.get("/rooms/{room_id}/users")
def get_users_in_room(room_id: str) -> list:
    def success_callback(response: database_pb2.GetUsersInRoomResponse):
        return [UserSchema(id=user.id, email=user.email) for user in response.users]

    return grpc_call(
        stub=database_stub,
        request=database_pb2.GetUsersInRoomRequest(room_id=room_id),
        success_callback=success_callback,
    )


@router.delete("/rooms/{room_id}/users/{user_id}")
def remove_user_from_room(room_id: str, user_id: str) -> str:
    def success_callback(response: database_pb2.RemoveUserFromRoomResponse):
        return response.user_id

    return grpc_call(
        stub=database_stub,
        request=database_pb2.RemoveUserFromRoomRequest(
            room_id=room_id,
            user_id=user_id,
        ),
        success_callback=success_callback,
    )


# ------------ Interfacing with MQTT ------------#


@router.post("/rooms/{room_id}/devices/{device_id}/command")
def post_command(room_id: str, device_id: str, controller: ControllerSchema):
    def success_callback(response: mqtt_pb2.PublishDeviceCommandResponse):
        return response

    return grpc_call(
        stub=mqtt_stub,
        request=mqtt_pb2.PublishDeviceCommandRequest(
            mqtt_pb2.Command(
                room_id=room_id,
                device_id=device_id,
                temperature=controller.temperature,
                fan_speed=controller.fan_speed,
            )
        ),
        success_callback=success_callback,
    )
