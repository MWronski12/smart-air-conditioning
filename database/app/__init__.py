from concurrent.futures import ThreadPoolExecutor
import grpc
import logging
from .database_servicer import DatabaseServicer
from .database_repository import DatabaseRepository


def serve(repository: DatabaseRepository, port=50051) -> None:
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    servicer = DatabaseServicer(repository)
    servicer.add_to_server(server)
    server.add_insecure_port(f"[::]:{port}")
    logging.info(f"Starting server on port {port}")
    server.start()
    server.wait_for_termination()
