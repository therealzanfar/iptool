"""Network Mask Related Code."""


import ipaddress
import re
from typing import Optional

from rich.console import Console

from iptool.utils import ordinal

IPV4_OCTET_COUNT = 4

NETMASK_OCTET_COUNT = IPV4_OCTET_COUNT
NETMASK_OCTET_VALUES = (0, 128, 192, 224, 240, 248, 252, 254, 255)
NETMASK_OCTET_BITS = {octet: bits for bits, octet in enumerate(NETMASK_OCTET_VALUES)}

HOSTMASK_OCTET_COUNT = IPV4_OCTET_COUNT
HOSTMASK_OCTET_VALUES = (255, 127, 63, 31, 15, 7, 3, 1, 0)
HOSTMASK_OCTET_BITS = {octet: bits for bits, octet in enumerate(HOSTMASK_OCTET_VALUES)}


RE_IPV4_MASKLEN_FRAGMENT = re.compile(
    r"^/?(?P<masklen>3[0-2]|[12][0-9]|0?[0-9])$",
)

re_netmask_octet = (
    rf"(?:{'|'.join(str(octet) for octet in reversed(NETMASK_OCTET_VALUES))})"
)
RE_IPV4_NETMASK_FRAGMENT = re.compile(
    rf"^(?:(?:255(?:\.255){{0,2}})?\.{re_netmask_octet}(?:\.0){{0,3}}|{re_netmask_octet}(?:\.0){{3}})$",
)

re_hostmask_octet = rf"(?:{'|'.join(str(octet) for octet in HOSTMASK_OCTET_VALUES)})"
RE_IPV4_HOSTMASK_FRAGMENT = re.compile(
    rf"^(?:(?:0(?:\.0){{0,2}})?\.{re_hostmask_octet}(?:\.255){{0,3}}|{re_hostmask_octet}(?:\.255){{3}})$",
)


def _parse_ipv4_masklen_fragment(fragment: str) -> int:
    m = RE_IPV4_MASKLEN_FRAGMENT.match(fragment)

    if not m:
        raise TypeError(f"Invalid CIDR Mask Length: {fragment}")

    return int(m.group("masklen"))


def _parse_ipv4_netmask_fragment(fragment: str) -> int:
    octets = [int(o) for o in fragment.split(".") if o != ""]

    assert len(octets) <= NETMASK_OCTET_COUNT

    while len(octets) < NETMASK_OCTET_COUNT:
        octets.insert(0, NETMASK_OCTET_VALUES[-1])

    mask_bits = 0
    for octet in octets:
        mask_bits += NETMASK_OCTET_BITS[octet]

    return mask_bits


def _parse_ipv4_hostmask_fragment(fragment: str) -> int:
    octets = [int(o) for o in fragment.split(".") if o != ""]

    assert len(octets) <= HOSTMASK_OCTET_COUNT

    while len(octets) < HOSTMASK_OCTET_COUNT:
        octets.insert(0, HOSTMASK_OCTET_VALUES[-1])

    mask_bits = 0
    for octet in octets:
        mask_bits += HOSTMASK_OCTET_BITS[octet]

    return mask_bits


def parse_mask_fragment(fragment: str) -> Optional[int]:
    """Parse the provided subnet fragment into a prefix length."""
    if RE_IPV4_MASKLEN_FRAGMENT.match(fragment):
        return _parse_ipv4_masklen_fragment(fragment)

    if RE_IPV4_NETMASK_FRAGMENT.match(fragment):
        return _parse_ipv4_netmask_fragment(fragment)

    if RE_IPV4_HOSTMASK_FRAGMENT.match(fragment):
        return _parse_ipv4_hostmask_fragment(fragment)

    return None


def print_ipv4_mask_table(
    start_prefix: int = 1,
    end_prefix: int = 32,
) -> None:
    """Print an IPv4 Subnet Table."""
    columns = [
        {
            "title": "Prefix",
            "size": 6,
            "color": "magenta",
        },
        {
            "title": "Netmask",
            "size": 15,
            "color": "green",
        },
        {
            "title": "Hostmask",
            "size": 15,
            "color": "yellow",
        },
        {
            "title": "Increment By",
            "size": 20,
            "color": "white",
        },
    ]

    for c in columns:
        if len(c["title"]) > c["size"]:
            c["size"] = len(c["title"])

    space_len = 2

    spaces = " " * space_len
    rowlen = sum(c["size"] for c in columns) + space_len * (len(columns) - 1)

    hfmt = spaces.join(f"{{:>{c['size']}s}}" for c in columns)
    rfmt = spaces.join(
        rf"[{c['color']}]{{:>{c['size']}s}}[/{c['color']}]" for c in columns
    )

    rprint = Console().print

    rprint(
        hfmt.format(*(c["title"] for c in columns)),
    )
    rprint("-" * rowlen)

    for s in range(start_prefix, end_prefix + 1):
        snet = ipaddress.ip_network(f"0.0.0.0/{s}")
        vals = (
            f"/{snet.prefixlen}",
            snet.netmask.exploded,
            snet.hostmask.exploded,
            f"{2**((32-s)%8):>3d} in the {ordinal((s-1)//8+1)} octet",
        )
        rprint(rfmt.format(*vals))
