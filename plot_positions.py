import datetime
import logging
import time

import arc852.cli_args  as cli
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
from arc852.constants import LOG_LEVEL, GRPC_HOST
from arc852.grpc_support import TimeoutException
from arc852.utils import setup_logging

from position_client import PositionClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = cli.setup_cli_args(cli.grpc_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    # Start position client
    with PositionClient(args[GRPC_HOST]) as positions:

        stream_ids = tls.get_credentials_file()['stream_ids']
        stream_id = stream_ids[1]

        # Declare graph
        graph = go.Scatter(x=[], y=[], mode='lines+markers', stream=dict(token=stream_id, maxpoints=80))
        data = go.Data([graph])
        layout = go.Layout(title='Line Offsets', yaxis=go.YAxis(range=[-400, 400]))
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='plot-positions')

        # Write data
        stream = py.Stream(stream_id)
        stream.open()

        logger.info("Opening plot.ly tab")
        time.sleep(5)

        prev_pos = None

        try:
            while True:
                try:
                    val = positions.get_position(timeout=0.5)

                    if not val.in_focus:
                        prev_pos = None
                        continue

                    y = val.mid_offset
                    prev_pos = y

                # No change in value
                except TimeoutException:
                    y = prev_pos

                x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                stream.write(dict(x=x, y=y))
                time.sleep(.10)

        except KeyboardInterrupt:
            pass
        finally:
            stream.close()

    logger.info("Exiting...")
