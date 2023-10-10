"""Subnet-Related Code."""


import ipaddress
import re
from typing import Optional

from iptool.utils import ordinal

IPv4_OCTET_COUNT = 4

SUBNET_OCTET_COUNT = IPv4_OCTET_COUNT
SUBNET_OCTET_VALUES = (0, 128, 192, 224, 240, 248, 252, 254, 255)
SUBNET_OCTET_BITS = {octet: bits for bits, octet in enumerate(SUBNET_OCTET_VALUES)}

WILDCARD_OCTET_COUNT = IPv4_OCTET_COUNT
WILDCARD_OCTET_VALUES = (255, 127, 63, 31, 15, 7, 3, 1, 0)
WILDCARD_OCTET_BITS = {octet: bits for bits, octet in enumerate(WILDCARD_OCTET_VALUES)}


RE_IPv4_CIDR_FRAGMENT = re.compile(
    r"^/?(?P<masklen>3[0-2]|[12][0-9]|0?[0-9])$",
)

re_subnet_octet = (
    rf"(?:{'|'.join(str(octet) for octet in reversed(SUBNET_OCTET_VALUES))})"
)
RE_IPv4_SUBNET_FRAGMENT = re.compile(
    rf"^(?:(?:255(?:\.255){{0,2}})?\.{re_subnet_octet}(?:\.0){{0,3}}|{re_subnet_octet}(?:\.0){{3}})$",
)

re_wildcard_octet = rf"(?:{'|'.join(str(octet) for octet in WILDCARD_OCTET_VALUES)})"
RE_IPv4_WILDCARD_FRAGMENT = re.compile(
    rf"^(?:(?:0(?:\.0){{0,2}})?\.{re_wildcard_octet}(?:\.255){{0,3}}|{re_wildcard_octet}(?:\.255){{3}})$",
)


def _parse_ipv4_cidr_masklen(fragment: str) -> int:
    m = RE_IPv4_CIDR_FRAGMENT.match(fragment)

    if not m:
        raise TypeError(f"Invalid CIDR Mask Length: {fragment}")

    return int(m.group("masklen"))


def _parse_ipv4_subnet_mask(fragment: str) -> int:
    octets = [int(o) for o in fragment.split(".") if o != ""]

    assert len(octets) <= SUBNET_OCTET_COUNT

    while len(octets) < SUBNET_OCTET_COUNT:
        octets.insert(0, SUBNET_OCTET_VALUES[-1])

    mask_bits = 0
    for octet in octets:
        mask_bits += SUBNET_OCTET_BITS[octet]

    return mask_bits


def _parse_ipv4_wildcard_mask(fragment: str) -> int:
    octets = [int(o) for o in fragment.split(".") if o != ""]

    assert len(octets) <= WILDCARD_OCTET_COUNT

    while len(octets) < WILDCARD_OCTET_COUNT:
        octets.insert(0, WILDCARD_OCTET_VALUES[-1])

    mask_bits = 0
    for octet in octets:
        mask_bits += WILDCARD_OCTET_BITS[octet]

    return mask_bits


def parse_subnet_fragment(fragment: str) -> Optional[int]:
    """Parse the provided subnet fragment into a prefix length."""
    if RE_IPv4_CIDR_FRAGMENT.match(fragment):
        return _parse_ipv4_cidr_masklen(fragment)

    if RE_IPv4_SUBNET_FRAGMENT.match(fragment):
        return _parse_ipv4_subnet_mask(fragment)

    if RE_IPv4_WILDCARD_FRAGMENT.match(fragment):
        return _parse_ipv4_wildcard_mask(fragment)

    return None


def print_ipv4_subnet_table(
    start_prefix: int = 1,
    end_prefix: int = 32,
) -> None:
    """Print an IPv4 Subnet Table."""
    columns = [
        {
            "title": "size",
            "size": 3,
        },
        {
            "title": "subnet mask",
            "size": 15,
        },
        {
            "title": "wildcard mask",
            "size": 15,
        },
        {
            "title": "subnet inc",
            "size": 20,
        },
    ]

    for c in columns:
        if len(c["title"]) > c["size"]:
            c["size"] = len(c["title"])

    rowlen = sum(c["size"] for c in columns) + (len(columns) - 1) * 3
    header_fmt = "   ".join([f"{{:>{c['size']}s}}" for c in columns])
    data_fmt = "   ".join([f"{{:>{c['size']}s}}" for c in columns])

    print(header_fmt.format(*[c["title"] for c in columns]))
    print("-" * rowlen)
    for s in range(start_prefix, end_prefix + 1):
        snet = ipaddress.ip_network(f"0.0.0.0/{s}")
        print(
            data_fmt.format(
                f"/{snet.prefixlen}",
                f"{snet.netmask.exploded}",
                f"{snet.hostmask.exploded}",
                f"{2**((32-s)%8)} in the {ordinal((s-1)//8+1)} octet",
            ),
        )
