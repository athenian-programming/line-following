#!/usr/bin/env python3

import logging

import arc852.cli_args  as cli
from arc852.cli_args import setup_cli_args
from arc852.constants import LOG_LEVEL, GRPC_HOST
from arc852.grpc_support import TimeoutException
from arc852.utils import setup_logging

from position_client import PositionClient

logger = logging.getLogger(__name__)


def main():
    # Parse CLI args
    args = setup_cli_args(cli.grpc_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    with PositionClient(args[GRPC_HOST]) as positions:
        try:
            while True:
                try:
                    print("Got position: {0}".format(positions.get_position(timeout=0.5)))
                except TimeoutException:
                    print("No change in value")
        except KeyboardInterrupt:
            pass

    logger.info("Exiting...")

if __name__ == "__main__":
    main()
