# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from app.protos import mqtt_pb2 as app_dot_protos_dot_mqtt__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class MqttServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PublishDeviceSettings = channel.unary_unary(
                '/mqtt.MqttService/PublishDeviceSettings',
                request_serializer=app_dot_protos_dot_mqtt__pb2.Settings.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class MqttServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PublishDeviceSettings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MqttServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PublishDeviceSettings': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishDeviceSettings,
                    request_deserializer=app_dot_protos_dot_mqtt__pb2.Settings.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mqtt.MqttService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MqttService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PublishDeviceSettings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mqtt.MqttService/PublishDeviceSettings',
            app_dot_protos_dot_mqtt__pb2.Settings.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
