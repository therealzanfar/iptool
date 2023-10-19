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

_re_ipv4_address_octet: str = r"(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]|[0-9])"
_re_ipv4_address: str = (
    rf"{_re_ipv4_address_octet}\.{_re_ipv4_address_octet}\."
    rf"{_re_ipv4_address_octet}\.{_re_ipv4_address_octet}"
)
RE_IPV4_ADDRESS: re.Pattern = re.compile(rf"\b{_re_ipv4_address}\b")

_re_ipv4_netmask_octet: str = r"(?:0|128|192|224|240|248|252|254)"
_re_ipv4_netmask_a: str = rf"{_re_ipv4_netmask_octet}\.0\.0\.0"
_re_ipv4_netmask_b: str = rf"255\.{_re_ipv4_netmask_octet}\.0\.0"
_re_ipv4_netmask_c: str = rf"255\.255.{_re_ipv4_netmask_octet}\.0"
_re_ipv4_netmask_d: str = rf"255\.255\.255\.{_re_ipv4_netmask_octet}"
_re_ipv4_netmask_e: str = r"255\.255\.255\.255"
_re_ipv4_netmask: str = (
    rf"(?:{_re_ipv4_netmask_a}|{_re_ipv4_netmask_b}|{_re_ipv4_netmask_c}"
    rf"|{_re_ipv4_netmask_d}|{_re_ipv4_netmask_e})"
)
RE_IPV4_NETMASK: re.Pattern = re.compile(rf"\b{_re_ipv4_netmask}\b")
RE_IPV4_SUBNET = RE_IPV4_NETMASK

# re_ipv4_hostmask_octet: str = re_ipv4_address_octet
# re_ipv4_hostmask_a: str = fr"{re_ipv4_hostmask_octet}\.255\.255\.255"
# re_ipv4_hostmask_b: str = fr"0.{re_ipv4_hostmask_octet}\.255\.255"
# re_ipv4_hostmask_c: str = fr"0\.0.{re_ipv4_hostmask_octet}\.255"
# re_ipv4_hostmask_d: str = fr"0\.0\.0\.{re_ipv4_hostmask_octet}"
# re_ipv4_hostmask: str = (
#     fr"(?:{re_ipv4_whostmask_a}|{re_ipv4_hostmask_b}|"
#     fr"{re_ipv4_hostmask_c}|{re_ipv4_hostmask_d})"
# )
RE_IPV4_HOSTMASK: re.Pattern = RE_IPV4_ADDRESS
RE_IPV4_WILDCARD = RE_IPV4_HOSTMASK

_re_ipv4_masklen: str = r"\/(?:[12]?[0-9]|3[0-2])"
RE_IPV4_INTERFACE: re.Pattern = re.compile(
    rf"\b{_re_ipv4_address}(?:\s+{_re_ipv4_netmask}|{_re_ipv4_masklen})\b",
)
RE_IPV4_NETWORK = RE_IPV4_INTERFACE

IP_VERSION_4 = 4
IP_VERSION_6 = 6


def parse_ip_addresses(text: str) -> Iterator[IPAddressT]:
    """Search a string for instances of IP Addresses."""
    for match in RE_IPV4_ADDRESS.finditer(text):
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
