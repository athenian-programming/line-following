import logging
import time
from threading import Thread

from common_constants import LOGGING_ARGS
from common_utils import sleep

from position_server import PositionServer


def test_position_server(port):
    server = PositionServer(port).start()
    for i in range(0, 100):
        server.write_position(in_focus=True if i % 2 == 0 else False,
                              mid_offset=i,
                              degrees=i + 1,
                              mid_line_cross=i + 2,
                              width=i + 3,
                              middle_inc=i + 4)
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(**LOGGING_ARGS)
    Thread(target=test_position_server, args=(50052,)).start()
    sleep()
