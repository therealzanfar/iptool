#! /usr/bin/env python3

"""Console Entry Point for `iptool` Mask Utility."""

import logging
import sys
from typing import Optional, cast

import click

from iptool.cli import CLICK_CONTEXT, setup_logging
from iptool.mask import parse_mask_fragment, print_ipv4_mask_table


@click.command(context_settings=CLICK_CONTEXT)
@click.option("-v", "--verbose", count=True)
@click.option("--show-all", "-a", is_flag=True, default=False)
@click.argument("MASK", default=None, required=False)
def cli_mask(
    mask: Optional[str] = None,
    show_all: bool = False,
    verbose: int = 0,
) -> int:
    """
    Print an IPv4 network mask chart.

    If you provide a subnet mask (netmask), wildcard mask (hostmask), or cidr
    prefix length (masklen), the table will show only that entry. Partial
    masks will be inferred.

    Without any arguments, the most-specific entries will be shown.

    If `--show-all` is provided, the entire 32-entry table is printed.
    """
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    if show_all:
        print_ipv4_mask_table()
        return 0

    if mask is not None:
        parsed_prefixlen = parse_mask_fragment(mask)

        if parsed_prefixlen is None:
            ctx = click.get_current_context()
            ctx.fail("Unknown subnet_size")

        print_ipv4_mask_table(
            cast(int, parsed_prefixlen),
            cast(int, parsed_prefixlen),
        )
        return 0

    print_ipv4_mask_table(20, 31)
    return 0


if __name__ == "__main__":
    sys.exit(cli_mask())
