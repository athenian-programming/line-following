#!/usr/bin/env python3

import logging

import cli_args  as cli
from cli_args import setup_cli_args
from grpc_support import TimeoutException
from utils import setup_logging

from position_client import PositionClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.grpc_host, cli.verbose)

    # Setup logging
    setup_logging(args["loglevel"])

    positions = PositionClient(args["grpc_host"]).start()

    try:
        while True:
            try:
                print("Got position: {0}".format(positions.get_position(timeout=0.5)))
            except TimeoutException:
                print("No change in value")
    except KeyboardInterrupt:
        pass
    finally:
        positions.stop()

    logger.info("Exiting...")
