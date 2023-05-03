import grpc
from typing import Dict, Any
from google.protobuf.json_format import MessageToDict

from .protos import database_pb2, database_pb2_grpc
from .database_repository import DatabaseRepository
from .exceptions import *


class DatabaseServicer(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self, repository: DatabaseRepository):
        self.repository = repository

    def __rpc_context_set(self, context, code, details):
        context.set_code(code)
        context.set_details(details)

    def add_to_server(self, server: grpc.Server):
        database_pb2_grpc.add_DatabaseServiceServicer_to_server(self, server)

    def AddRoom(self, request: database_pb2.AddRoomRequest, context):
        try:
            room = self.repository.add_room(
                MessageToDict(request.room, preserving_proto_field_name=True)
            )
        except RoomAlreadyExistsError as e:
            self.__rpc_context_set(context, grpc.StatusCode.ALREADY_EXISTS, str(e))
            return database_pb2.AddRoomResponse()

        return database_pb2.AddRoomResponse(room=database_pb2.Room(**room))

    def GetRoom(self, request: database_pb2.GetRoomRequest, context):
        try:
            room = self.repository.get_room(request.id)
        except RoomNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.GetRoomResponse()
        return database_pb2.GetRoomResponse(room=database_pb2.Room(**room))

    def GetAllRooms(self, request: database_pb2.GetAllRoomsRequest, context):
        rooms = self.repository.get_all_rooms()
        return database_pb2.GetAllRoomsResponse(rooms=[database_pb2.Room(**room) for room in rooms])

    def AddDevice(self, request: database_pb2.AddDeviceRequest, context):
        try:
            device = self.repository.add_device(
                request.room_id, MessageToDict(request.device, preserving_proto_field_name=True)
            )
        except DeviceAlreadyExistsError as e:
            self.__rpc_context_set(context, grpc.StatusCode.ALREADY_EXISTS, str(e))
            return database_pb2.AddDeviceResponse()
        except RoomNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.AddDeviceResponse()

        return database_pb2.AddDeviceResponse(device=database_pb2.Device(**device))

    def GetDevicesInRoom(self, request: database_pb2.GetDevicesInRoomRequest, context):
        try:
            devices = self.repository.get_devices_in_room(request.room_id)
        except RoomNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.AddDeviceResponse()

        return database_pb2.GetDevicesInRoomResponse(
            devices=[database_pb2.Device(**device) for device in devices]
        )

    def AddUser(self, request: database_pb2.AddUserRequest, context):
        try:
            user = self.repository.add_user(
                MessageToDict(request.user, preserving_proto_field_name=True)
            )
        except UserAlreadyExistsError as e:
            self.__rpc_context_set(context, grpc.StatusCode.ALREADY_EXISTS, str(e))
            return database_pb2.AddUserResponse()

        if "preferences" not in user:
            user["preferences"] = {}

        return database_pb2.AddUserResponse(
            user=database_pb2.User(
                id=user["id"],
                email=user["email"],
                preferences=database_pb2.Preference(**user["preferences"]),
            )
        )

    def GetUser(self, request: database_pb2.GetUserRequest, context):
        try:
            user = self.repository.get_user(request.id)
        except UserNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.GetUserResponse()

        if "preferences" not in user:
            user["preferences"] = {}

        return database_pb2.GetUserResponse(
            user=database_pb2.User(
                id=user["id"],
                email=user["email"],
                preferences=database_pb2.Preference(**user["preferences"]),
            )
        )

    def SetUserPreferences(self, request: database_pb2.SetUserPreferencesRequest, context):
        try:
            preferences = self.repository.set_user_preferences(
                request.user_id,
                MessageToDict(request.preferences, preserving_proto_field_name=True),
            )
        except UserNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.GetUserResponse()

        return database_pb2.SetUserPreferencesResponse(
            preferences=database_pb2.Preference(**preferences)
        )

    def AddUserToRoom(self, request: database_pb2.AddUserToRoomRequest, context):
        try:
            self.repository.add_user_to_room(request.user_id, request.room_id)
        except (UserNotFoundError, RoomNotFoundError) as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
        finally:
            return database_pb2.AddUserToRoomResponse()

    def RemoveUserFromRoom(self, request: database_pb2.RemoveUserFromRoomRequest, context):
        try:
            self.repository.remove_user_from_room(request.user_id, request.room_id)
        except (UserNotFoundError, RoomNotFoundError) as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
        finally:
            return database_pb2.RemoveUserFromRoomResponse()

    def GetUsersInRoom(self, request: database_pb2.GetUsersInRoomRequest, context):
        try:
            users = self.repository.get_users_in_room(request.room_id)
        except RoomNotFoundError as e:
            self.__rpc_context_set(context, grpc.StatusCode.NOT_FOUND, str(e))
            return database_pb2.GetUsersInRoomResponse()

        return database_pb2.GetUsersInRoomResponse(
            users=[
                database_pb2.User(
                    id=user["id"],
                    email=user["email"],
                    preferences=database_pb2.Preference(**user["preferences"]),
                )
                for user in users
            ]
        )
