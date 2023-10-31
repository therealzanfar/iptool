#! /usr/bin/env python3

"""Console Entry Point for `iptool` Summarization Utility."""

import logging
import sys

import click

from iptool.cli import CLICK_CONTEXT, rprint, setup_logging
from iptool.ip import IPNetworkT, parse_ip_networks, summarize_ip_networks


def read_ips_from_stdin() -> list[IPNetworkT]:
    """Read STDIN lines as IP networks."""
    return []


@click.command(context_settings=CLICK_CONTEXT)
@click.argument("NETWORK", nargs=-1)
@click.option(
    "-Y",
    "--stdin",
    is_flag=True,
    flag_value=True,
    type=bool,
    help="Read from STDIN even if arguments are provided.",
)
@click.option(
    "-N",
    "--no-stdin",
    is_flag=True,
    flag_value=True,
    type=bool,
    help=(
        "Disables reading from STDIN, even if no arguments are provided. "
        "Useful for scripts or unattended execution as it will not block."
    ),
)
@click.option("-v", "--verbose", count=True)
def cli_summarize(
    network: list[str],
    stdin: bool = False,
    no_stdin: bool = False,
    verbose: int = 0,
) -> int:
    """
    Summarize IP Addresses and Networks.

    Read any number of IPv4 or IPv6 Addresses or Networks from arguments or
    STDIN and generate a minimal list of networks that cover *exactly* the
    same space. STDIN Addresses and networks should be line-break-separated
    (one per line). Networks specified by netmask or hostmask may have the
    address and mask separated by a slash ("/", like CIDR notation).

    If no arguments are provided, STDIN is read by default unless --no-stdin
    is also provided.

    If arguments are provided, STDIN is ignored unless --stdin is also
    provided.

    If both --stdin and --no-stdin are provided, STDIN will be ignored.
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    networks: list[IPNetworkT] = []

    read_stdin = stdin and not no_stdin
    if len(network) <= 0 and not no_stdin:
        logger.info("No arguments provided, reading from STDIN")
        read_stdin = True

    networks.extend(parse_ip_networks(network))
    if read_stdin:
        networks.extend(parse_ip_networks(sys.stdin))

    summaries = summarize_ip_networks(networks)

    for s in summaries:
        rprint(s.compressed)


if __name__ == "__main__":
    sys.exit(cli_summarize())
