from concurrent import futures

import grpc

from grebble_flow.grpc.processor import processor_pb2_grpc
from grebble_flow.grpc.processor.service import ProcessorService


def start_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    processor_pb2_grpc.add_ProcessorServicer_to_server(ProcessorService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print('Server started')
    server.wait_for_termination()
