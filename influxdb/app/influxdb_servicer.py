import grpc

from .protos import influxdb_pb2, influxdb_pb2_grpc

class InfluxDBServicer(influxdb_pb2_grpc.InfluxdbServiceServicer):
    def __init__(self):
        pass

    def __rpc_context_set(self, context, code, details):
        context.set_code(code)
        context.set_details(details)

    def add_to_server(self, server: grpc.Server):
        influxdb_pb2_grpc.add_InfluxdbServiceServicer_to_server(self, server)
    
    def WriteMeasurement(self, request: influxdb_pb2.WriteMeasurementRequest, context):
        pass

    def ReadMeasurements(self, request: influxdb_pb2.ReadMeasurementsRequest, context):
        pass