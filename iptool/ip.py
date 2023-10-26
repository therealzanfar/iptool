"""
IP-Related Utilities.

Some functions are limited to IPv4 at the moment.
"""

import logging
import re
from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
    ip_interface,
)
from typing import Iterable, Iterator, Optional, Tuple, Union, overload

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

IPv4ObjectT = Union[
    IPv4Address,
    IPv4Interface,
    IPv4Network,
]

IPv6ObjectT = Union[
    IPv6Address,
    IPv6Interface,
    IPv6Network,
]

_re_ipv4_address_octet: str = r"(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]|[0-9])"
_re_ipv4_address: str = (
    rf"{_re_ipv4_address_octet}\.{_re_ipv4_address_octet}\."
    rf"{_re_ipv4_address_octet}\.{_re_ipv4_address_octet}"
)
RE_IPV4_ADDRESS: re.Pattern = re.compile(rf"\b(?P<address>{_re_ipv4_address})\b")

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

_re_ipv4_masklen: str = r"(?:[12]?[0-9]|3[0-2])"
RE_IPV4_INTERFACE: re.Pattern = re.compile(
    rf"\b(?P<address>{_re_ipv4_address})(?:\s+|\/)(?P<mask>{_re_ipv4_netmask}|{_re_ipv4_masklen})\b",
)
RE_IPV4_NETWORK = RE_IPV4_INTERFACE

IP_VERSION_4 = 4
IP_VERSION_6 = 6


def parse_ip_addresses(text: str) -> Iterator[IPAddressT]:
    """Search a string for instances of IP Addresses."""
    for match in RE_IPV4_ADDRESS.finditer(text):
        yield IPv4Address(match.group(0))


def parse_ip_object(text: str) -> IPObjectT:
    """Find an IP Address, Network, or Interface in a string."""
    logger = logging.getLogger(__name__)
    text = text.strip()

    if m := RE_IPV4_INTERFACE.search(text):
        addr = f"{m.group('address')}/{m.group('mask')}"

        try:
            obj = IPv4Network(addr)
            logger.debug(f"{text} appears to be an IPv4 Network")
            return obj
        except (AddressValueError, ValueError):
            pass

        try:
            obj = IPv4Interface(addr)
            logger.debug(f"{text} appears to be an IPv4 Interface")
            return obj
        except (AddressValueError, ValueError):
            pass

    if m := RE_IPV4_ADDRESS.search(text):
        logger.debug(f"{text} appears to be an IPv4 Address")
        return IPv4Address(m.group("address"))

    try:
        obj = IPv6Network(text.strip())
        logger.debug(f"{text} appears to be an IPv6 Network")
        return obj
    except (AddressValueError, ValueError):
        pass

    try:
        obj = IPv6Interface(text.strip())
        logger.debug(f"{text} appears to be an IPv6 Interface")
        return obj
    except (AddressValueError, ValueError):
        pass

    try:
        obj = IPv6Address(text.strip())
        logger.debug(f"{text} appears to be an IPv6 Address")
        return obj
    except (AddressValueError, ValueError):
        pass

    raise ValueError(f"Unable to find IP Address or Interface in '{text}'")


def to_ip_network(obj: IPObjectT) -> IPNetworkT:
    """Convert any IP Object to an IP Network."""
    if isinstance(obj, (IPv4Network, IPv6Network)):
        return obj

    if isinstance(obj, (IPv4Interface, IPv6Interface)):
        return obj.network

    if isinstance(obj, IPv4Address):
        return IPv4Network(f"{obj.compressed}/{obj.max_prefixlen}")

    if isinstance(obj, IPv6Address):
        return IPv6Address(f"{obj.compressed}/{obj.max_prefixlen}")

    raise TypeError(f"Unable to convert type {type(obj)}")


def parse_ip_networks(seq: Iterable[str]) -> list[IPNetworkT]:
    """Extract IP Objects from an iterable, and return the IP Network representation."""
    logger = logging.getLogger(__name__)

    networks: list[IPNetworkT] = []

    for item in seq:
        try:
            networks.append(to_ip_network(parse_ip_object(item)))
        except ValueError:
            logger.warning(f"Cannot parse IP Object from '{item}")

    return sorted(networks, key=ip_object_sort_key)


@overload
def filter_ipv4_objects(seq: Iterable[IPAddressT]) -> list[IPv4Address]:
    ...


@overload
def filter_ipv4_objects(seq: Iterable[IPNetworkT]) -> list[IPv4Network]:
    ...


@overload
def filter_ipv4_objects(seq: Iterable[IPInterfaceT]) -> list[IPv4Interface]:
    ...


@overload
def filter_ipv4_objects(seq: Iterable[IPObjectT]) -> list[IPv4ObjectT]:
    ...


def filter_ipv4_objects(seq):
    """Extract IPv6 Objects from an iterable."""
    return sorted((n for n in seq if n.version == IP_VERSION_4), key=ip_object_sort_key)


@overload
def filter_ipv6_objects(seq: Iterable[IPAddressT]) -> list[IPv6Address]:
    ...


@overload
def filter_ipv6_objects(seq: Iterable[IPNetworkT]) -> list[IPv6Network]:
    ...


@overload
def filter_ipv6_objects(seq: Iterable[IPInterfaceT]) -> list[IPv6Interface]:
    ...


@overload
def filter_ipv6_objects(seq: Iterable[IPObjectT]) -> list[IPv6ObjectT]:
    ...


def filter_ipv6_objects(seq):
    """Extract IPv6 Objects from an iterable."""
    return sorted((n for n in seq if n.version == IP_VERSION_6), key=ip_object_sort_key)


def normalize_ip_interface(
    addr: str,
    mask: Optional[str] = None,
) -> Optional[IPInterfaceT]:
    """Parse a string representation of a network address and optional mask."""
    net_id = addr

    if mask is not None:
        if mask.startswith("/"):
            net_id += mask
        else:
            net_id += f"/{mask}"

    try:
        return ip_interface(net_id)
    except AddressValueError:
        return None


def parse_ip_network(addr: str, mask: Optional[str] = None) -> Optional[IPNetworkT]:
    """Parse a string representation of a network address and optional mask."""
    net_id = normalize_ip_interface(addr, mask)

    if net_id is not None:
        return net_id.network

    return None


def ip_object_sort_key(obj: IPObjectT) -> Tuple[int, int, int, int]:
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
