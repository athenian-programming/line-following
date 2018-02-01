import logging
import socket

import grpc
from arc852.grpc_support import CannotConnectException
from arc852.grpc_support import grpc_url
from arc852.utils import setup_logging
from proto.position_server_pb2 import ClientInfo
from proto.position_server_pb2 import PositionServerStub

logger = logging.getLogger(__name__)


class Positions(object):
    def __init__(self, hostname):
        self.__url = grpc_url(hostname)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def start(self):
        try:
            channel = grpc.insecure_channel(self.__url)
            self._stub = PositionServerStub(channel)
            self._client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
            self._server_info = self._stub.registerClient(self._client_info)
        except grpc._channel._Rendezvous:
            raise CannotConnectException(self.__url)

    def values(self):
        return self._stub.getPositions(self._client_info)


if __name__ == "__main__":
    setup_logging()
    with Positions("localhost") as positions:
        for val in positions.values():
            logger.info("Read value:\n%s", val)
    logger.info("Exiting...")
