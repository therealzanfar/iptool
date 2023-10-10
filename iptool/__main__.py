#! /usr/bin/env python3

"""Console Entry Point for iptool Utility."""

import logging
import sys

import click
from click_default_group import DefaultGroup

from iptool.cli import CLICK_CONTEXT, setup_logging
from iptool.subnet.__main__ import cli_subnet


@click.group(
    context_settings=CLICK_CONTEXT,
    cls=DefaultGroup,
    default="subnet",
    default_if_no_args=True,
)
@click.option("-v", "--verbose", count=True)
def cli_main(verbose: int = 0) -> int:
    """
    CLI Tools for Managing IP Addresses and Related Objects.

    Use `iptool COMMAND --help` for help with a specific utility.
    If no COMMAND is provided, the "subnet" utility is used by default.
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    return 0


cli_main.add_command(cli_subnet, name="subnet")

if __name__ == "__main__":
    sys.exit(cli_main())
