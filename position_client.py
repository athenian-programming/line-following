import logging
import socket
import time
from threading import Event

import grpc
from grpc_support import GenericClient
from grpc_support import TimeoutException

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import FocusLinePositionServerStub

logger = logging.getLogger(__name__)


class PositionClient(GenericClient):
    def __init__(self, hostname):
        super(PositionClient, self).__init__(hostname, "position client")
        self.__ready = Event()
        self.__id = -1
        self.__in_focus = False
        self.__mid_offset = -1
        self.__degrees = -1
        self.__mid_cross = -1
        self.__width = -1
        self.__middle_inc = -1

    def _mark_ready(self):
        self.__ready.set()

    def _get_values(self, pause_secs=2.0):
        channel = grpc.insecure_channel(self._hostname)
        stub = FocusLinePositionServerStub(channel)
        while not self.stopped:
            logger.info("Connecting to gRPC server at {0}...".format(self._hostname))
            try:
                client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
                server_info = stub.registerClient(client_info)
            except BaseException as e:
                logger.error("Failed to connect to gRPC server at {0} [{1}]".format(self._hostname, e))
                time.sleep(pause_secs)
                continue

            logger.info("Connected to gRPC server at {0} [{1}]".format(self._hostname, server_info.info))
            try:
                for val in stub.getFocusLinePositions(client_info):
                    with self.value_lock:
                        self.__id = val.id
                        self.__in_focus = val.in_focus
                        self.__mid_offset = val.mid_offset
                        self.__degrees = val.degrees
                        self.__mid_cross = val.mid_line_cross
                        self.__width = val.width
                        self.__middle_inc = val.middle_inc
                    self._mark_ready()
            except BaseException as e:
                logger.info("Disconnected from gRPC server at {0} [{1}]".format(self._hostname, e))
                time.sleep(pause_secs)

    # Blocking
    def get_position(self, timeout=None):
        while not self.stopped:
            if not self.__ready.wait(timeout):
                raise TimeoutException
            with self.value_lock:
                if self.__ready.is_set() and not self.stopped:
                    self.__ready.clear()
                    return {"id": self.__id,
                            "in_focus": self.__in_focus,
                            "mid_offset": self.__mid_offset,
                            "degrees": self.__degrees,
                            "mid_cross": self.__mid_cross,
                            "width": self.__width,
                            "middle_inc": self.__middle_inc}
