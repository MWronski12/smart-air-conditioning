import grpc
from .protos import logic_pb2, logic_pb2_grpc
from .logic import *


class LogicServicer(logic_pb2_grpc.LogicServiceServicer):
    def __init__(self) -> None:
        pass

    def add_to_server(self, server: grpc.Server) -> None:
        logic_pb2_grpc.add_LogicServiceServicer_to_server(self, server)

    def NotifyUserPreferenceChange(self, request: logic_pb2.NotifyUserPreferenceChangeRequest, context):
        room = get_user_room(request.user_id).room
        if room != None:
            update_room_preferences(room.id)
        return logic_pb2.NotifyUserPreferenceChangeResponse(user_id=request.user_id)

    def NotifyUserRoomChange(self, request: logic_pb2.NotifyUserRoomChangeRequest, context):
        update_room_preferences(request.room_id)
        return logic_pb2.NotifyUserRoomChangeResponse(user_id=request.user_id, room_id=request.room_id)
