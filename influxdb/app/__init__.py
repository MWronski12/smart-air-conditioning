from concurrent.futures import ThreadPoolExecutor
import grpc
import logging
from influxdb_client import InfluxDBClient
from .influxdb_servicer import InfluxDBServicer
from .inflxudb import InfluxDB
from .config import INFLUXDB_HOST, INFLUXDB_TOKEN, INFLUXDB_ORG


def serve(port=50051) -> None:
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    servicer = InfluxDBServicer(
        InfluxDBClient(
            url=INFLUXDB_HOST,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG,
        )
    )
    servicer.add_to_server(server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"Starting server on port {port}")
    server.start()
    server.wait_for_termination()
