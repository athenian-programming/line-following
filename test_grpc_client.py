from __future__ import print_function

import socket
from threading import Thread

import grpc
from utils import setup_logging
from utils import sleep

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import FocusLinePositionServerStub


def read_positions(hostname):
    channel = grpc.insecure_channel(hostname)
    stub = FocusLinePositionServerStub(channel)
    client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
    server_info = stub.registerClient(client_info)

    for pos in stub.getFocusLinePositions(client_info):
        print("Received position {0}".format(pos))

    print("Disconnected from gRPC server at {0}".format(hostname))


if __name__ == "__main__":
    setup_logging()
    Thread(target=read_positions, args=("localhost:50052",)).start()
    sleep()
