#! /usr/bin/env python3

"""Console Entry Point for `iptool` Subnet Utility."""

import logging
import sys
from typing import Optional

import click

from iptool.cli import CLICK_CONTEXT, setup_logging
from iptool.ip import normalize_ip_interface
from iptool.subnet import print_subnet_info


@click.command(context_settings=CLICK_CONTEXT)
@click.argument("NET_ID")
@click.argument("MASK", default=None, required=False)
@click.option("-v", "--verbose", count=True)
def cli_subnet(
    net_id: str,
    mask: Optional[str] = None,
    verbose: int = 0,
) -> int:
    """
    Show details about an IP subnet.

    A Network Address (IP) and Network Mask (subnet) are both required. For
    IPv4 networks, the mask can be specified either in CIDR notation (masklen)
    or as a separate netmask or hostmask. IPv6 networks must use the CIDR
    notation.
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    interface = normalize_ip_interface(net_id, mask)
    if interface is None:
        ctx = click.get_current_context()
        ctx.fail("Invalid network address and/or mask")

    print_subnet_info(interface)


if __name__ == "__main__":
    sys.exit(cli_subnet())
