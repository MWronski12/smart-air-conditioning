import grpc
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging


from .protos import influxdb_pb2, influxdb_pb2_grpc
from .config import INFLUXDB_BUCKET, INFLUXDB_ORG


class InfluxDBServicer(influxdb_pb2_grpc.InfluxdbServiceServicer):
    def __init__(self, influxdb_client: InfluxDBClient):
        self.influxdb_client = influxdb_client

    def __rpc_context_set(self, context, code, details):
        context.set_code(code)
        context.set_details(details)

    def add_to_server(self, server: grpc.Server):
        influxdb_pb2_grpc.add_InfluxdbServiceServicer_to_server(self, server)

    def WriteMeasurement(self, request: influxdb_pb2.WriteMeasurementRequest, context):
        logging.info(f"Received measurement: {request.measurement}")
        try:
            point = (
                Point("temperature")
                .tag("room_id", request.measurement.room_id)
                .tag("device_id", request.measurement.device_id)
                .field("value", request.measurement.temperature)
            )
            write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)
            point = (
                Point("humidity")
                .tag("room_id", request.measurement.room_id)
                .tag("device_id", request.measurement.device_id)
                .field("value", request.measurement.humidity)
            )
            write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        except Exception as e:
            self.__rpc_context_set(context, grpc.StatusCode.INTERNAL, str(e))
        finally:
            return influxdb_pb2.WriteMeasurementResponse()

    def ReadMeasurements(self, request: influxdb_pb2.ReadMeasurementsRequest, context):
        query = f'from(bucket: "{INFLUXDB_BUCKET}") \
        |> range(start: -12h) \
        |> filter(fn: (r) \
            => r.device_id == "{request.device_id}" \
            and r.room_id == "{request.room_id}")'

        tables = self.influxdb_client.query_api().query(org=INFLUXDB_ORG, query=query)
        temperature_list = list()
        humidity_list = list()

        measurements = list()

        for table in tables:
            measurement = influxdb_pb2.Measurement()
            for record in table.records:
                data_type = record.get_field()
                timestamp = record.get_time()
                if data_type == "temperature":
                    measurement.temperature = record.get_value()
                elif data_type == "humidity":
                    measurement.humidity = record.get_value()
            measurements.append(measurement)

        logging.info(f"Sending measurements: {measurements}")

        return influxdb_pb2.ReadMeasurementsResponse(measurement=measurements)
