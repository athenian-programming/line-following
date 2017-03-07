from __future__ import print_function

import copy
import logging
import socket
import time
from threading import Event

import grpc
from grpc_support import GenericClient
from grpc_support import TimeoutException
from utils import setup_logging

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import FocusLinePositionServerStub

logger = logging.getLogger(__name__)


class PositionClient(GenericClient):
    def __init__(self, hostname):
        super(PositionClient, self).__init__(hostname, desc="position client")
        self.__ready = Event()
        self.__currval = None

    def _mark_ready(self):
        self.__ready.set()

    def _get_values(self, pause_secs=2.0):
        channel = grpc.insecure_channel(self.hostname)
        stub = FocusLinePositionServerStub(channel)
        while not self.stopped:
            logger.info("Connecting to gRPC server at {0}...".format(self.hostname))
            try:
                client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
                server_info = stub.registerClient(client_info)
            except BaseException as e:
                logger.error("Failed to connect to gRPC server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)
                continue

            logger.info("Connected to gRPC server at {0} [{1}]".format(self.hostname, server_info.info))
            try:
                for val in stub.getFocusLinePositions(client_info):
                    with self.value_lock:
                        self.__currval = copy.deepcopy(val)
                    self._mark_ready()
            except BaseException as e:
                logger.info("Disconnected from gRPC server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)

    # Blocking
    def get_position(self, timeout=None):
        while not self.stopped:
            if not self.__ready.wait(timeout):
                raise TimeoutException
            with self.value_lock:
                if self.__ready.is_set() and not self.stopped:
                    self.__ready.clear()
                    return self.__currval


if __name__ == "__main__":
    setup_logging()

    channel = grpc.insecure_channel("localhost")
    stub = FocusLinePositionServerStub(channel)
    client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
    server_info = stub.registerClient(client_info)

    for val in stub.getFocusLinePositions(client_info):
        print("Received position {0}".format(val))

    print("Disconnected from gRPC server")
