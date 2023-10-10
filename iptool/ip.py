"""
IP-Related Utilities.

Some functions are limited to IPv4 at the moment.
"""

import re
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Iterator, Tuple, Union

IPObjectT = Union[
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
]
IPAddressT = Union[IPv4Address, IPv6Address]
IPInterfaceT = Union[IPv4Interface, IPv6Interface]
IPNetworkT = Union[IPv4Network, IPv6Network]

_re_ip4_addr_octet: str = r"(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]|[0-9])"
_re_ip4_addr: str = (
    rf"{_re_ip4_addr_octet}\.{_re_ip4_addr_octet}\."
    rf"{_re_ip4_addr_octet}\.{_re_ip4_addr_octet}"
)
RE_IPv4_ADDR: re.Pattern = re.compile(rf"\b{_re_ip4_addr}\b")

_re_ip4_subnet_octet: str = r"(?:0|128|192|224|240|248|252|254)"
_re_ip4_subnet_a: str = rf"{_re_ip4_subnet_octet}\.0\.0\.0"
_re_ip4_subnet_b: str = rf"255\.{_re_ip4_subnet_octet}\.0\.0"
_re_ip4_subnet_c: str = rf"255\.255.{_re_ip4_subnet_octet}\.0"
_re_ip4_subnet_d: str = rf"255\.255\.255\.{_re_ip4_subnet_octet}"
_re_ip4_subnet_e: str = r"255\.255\.255\.255"
_re_ip4_subnet: str = (
    rf"(?:{_re_ip4_subnet_a}|{_re_ip4_subnet_b}|{_re_ip4_subnet_c}"
    rf"|{_re_ip4_subnet_d}|{_re_ip4_subnet_e})"
)
RE_IPv4_SUBNET: re.Pattern = re.compile(rf"\b{_re_ip4_subnet}\b")

# re_ip4_wildcard_octet: str = re_ip4_addr_octet
# re_ip4_wildcard_a: str = fr"{re_ip4_wildcard_octet}\.255\.255\.255"
# re_ip4_wildcard_b: str = fr"0.{re_ip4_wildcard_octet}\.255\.255"
# re_ip4_wildcard_c: str = fr"0\.0.{re_ip4_wildcard_octet}\.255"
# re_ip4_wildcard_d: str = fr"0\.0\.0\.{re_ip4_wildcard_octet}"
# re_ip4_wildcard: str = (
#     fr"(?:{re_ip4_wildcard_a}|{re_ip4_wildcard_b}|"
#     fr"{re_ip4_wildcard_c}|{re_ip4_wildcard_d})"
# )
RE_IPv4_WILDCARD: re.Pattern = RE_IPv4_ADDR

_re_ipv4_cidr: str = r"\/(?:[12]?[0-9]|3[0-2])"
RE_IPv4_INTERFACE: re.Pattern = re.compile(
    rf"\b{_re_ip4_addr}(?:\s+{_re_ip4_subnet}|{_re_ipv4_cidr})\b",
)


def parse_ip_addresses(text: str) -> Iterator[IPAddressT]:
    """Search a string for instances of IP Addresses."""
    for match in RE_IPv4_ADDR.finditer(text):
        yield IPv4Address(match.group(0))


def sort_ip_objects(obj: IPObjectT) -> Tuple[int, int, int, int]:
    """
    Universal key for sorting diverse IP objects.

    use:
        sorted(objects, key=sort_ip_objects)
        objects.sort(key=sort_ip_objects)
    """
    if isinstance(obj, (IPv4Address, IPv6Address)):
        mask = 32
        key = int(obj)
        is_net = 0
    elif isinstance(obj, (IPv4Network, IPv6Network)):
        mask = obj.prefixlen
        key = int(obj.network_address)
        is_net = 1
    elif isinstance(obj, (IPv4Interface, IPv6Interface)):
        mask = obj.network.prefixlen
        key = int(obj.ip)
        is_net = 1

    else:
        raise TypeError(
            f"Cannot sort objects of type {type(obj)} with this function",
        )

    return (obj.version, is_net, mask, key)
