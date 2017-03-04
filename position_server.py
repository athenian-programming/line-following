import logging
import time

import grpc
from concurrent import futures
from grpc_support import GenericServer

from gen.grpc_server_pb2 import FocusLinePosition
from gen.grpc_server_pb2 import FocusLinePositionServerServicer
from gen.grpc_server_pb2 import ServerInfo
from gen.grpc_server_pb2 import add_FocusLinePositionServerServicer_to_server

logger = logging.getLogger(__name__)

class PositionServer(FocusLinePositionServerServicer, GenericServer):
    def __init__(self, port):
        super(PositionServer, self).__init__(port, "position server")
        self._grpc_server = None

    def registerClient(self, request, context):
        logger.info("Connected to {0} client {1} [{2}]".format(self.desc, context.peer(), request.info))
        with self.cnt_lock:
            self._invoke_cnt += 1
        return ServerInfo(info="Server invoke count {0}".format(self._invoke_cnt))

    def getFocusLinePositions(self, request, context):
        client_info = request.info
        return self.currval_generator(context.peer())

    def _init_values_on_start(self):
        self.write_position(False, -1, -1, -1, -1, -1)

    def _start_server(self):
        logger.info("Starting gRPC {0} listening on {1}".format(self.desc, self._hostname))
        self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_FocusLinePositionServerServicer_to_server(self, self._grpc_server)
        self._grpc_server.add_insecure_port(self._hostname)
        self._grpc_server.start()
        try:
            while not self.stopped:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def write_position(self, in_focus, mid_offset, degrees, mid_line_cross, width, middle_inc):
        if not self.stopped:
            self.set_currval(FocusLinePosition(id=self._id,
                                               in_focus=in_focus,
                                               mid_offset=mid_offset,
                                               degrees=degrees,
                                               mid_line_cross=mid_line_cross,
                                               width=width,
                                               middle_inc=middle_inc))
            self._id += 1
