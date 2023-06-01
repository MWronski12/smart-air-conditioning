# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from app.protos import logic_pb2 as app_dot_protos_dot_logic__pb2


class LogicServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NotifyUserPreferenceChange = channel.unary_unary(
                '/logic.LogicService/NotifyUserPreferenceChange',
                request_serializer=app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeRequest.SerializeToString,
                response_deserializer=app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeResponse.FromString,
                )
        self.NotifyUserRoomChange = channel.unary_unary(
                '/logic.LogicService/NotifyUserRoomChange',
                request_serializer=app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeRequest.SerializeToString,
                response_deserializer=app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeResponse.FromString,
                )


class LogicServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NotifyUserPreferenceChange(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NotifyUserRoomChange(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NotifyUserPreferenceChange': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyUserPreferenceChange,
                    request_deserializer=app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeRequest.FromString,
                    response_serializer=app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeResponse.SerializeToString,
            ),
            'NotifyUserRoomChange': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyUserRoomChange,
                    request_deserializer=app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeRequest.FromString,
                    response_serializer=app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'logic.LogicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LogicService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NotifyUserPreferenceChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/logic.LogicService/NotifyUserPreferenceChange',
            app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeRequest.SerializeToString,
            app_dot_protos_dot_logic__pb2.NotifyUserPreferenceChangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NotifyUserRoomChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/logic.LogicService/NotifyUserRoomChange',
            app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeRequest.SerializeToString,
            app_dot_protos_dot_logic__pb2.NotifyUserRoomChangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
