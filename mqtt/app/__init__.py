from concurrent.futures import ThreadPoolExecutor
import grpc
import logging
from .mqtt_servicer import MqttServicer


def serve(port=50051) -> None:
    logging.basicConfig(level=logging.DEBUG)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    servicer = MqttServicer()
    servicer.add_to_server(server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"Starting server on port {port}")
    server.start()
    server.wait_for_termination()
