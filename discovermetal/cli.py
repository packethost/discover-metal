#!/usr/bin/python3

import os
import sys
import time
import json
import click
import logging
import threading
from datetime import datetime
from discovermetal import DiscoverMetal
from discovermetal.discover import now


@click.command()
@click.option("-s", "--send", help="Send the data to this location")
@click.option(
    "-q", "--quiet", default=False, is_flag=True, help="Provide more detailed output"
)
@click.option("-v", "--verbose", count=True, help="Provide more detailed output")
def cli(send, quiet, verbose):
    level = logging.WARNING
    if verbose:
        valid_levels = [logging.INFO, logging.WARNING, logging.DEBUG]
        try:
            level = valid_levels[verbose - 1]
            # Ignore urllib3 DEBUG messages
            urllib3_log = logging.getLogger("urllib3")
            urllib3_log.setLevel(logging.WARNING)
        except IndexError:
            # If 4 or more 'v', enable debug, and don't ignore urllib3
            level = logging.DEBUG
    if not quiet:
        logging.basicConfig(level=level, stream=sys.stdout)

    pd = DiscoverMetal()
    pd.run()
    print(json.dumps(pd.flatten(), indent=2))
    if send:
        pd.send(send)
