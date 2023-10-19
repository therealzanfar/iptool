"""Network Subnet Related Code."""

from iptool.ip import IP_VERSION_4, IPInterfaceT, IPNetworkT
from iptool.utils import approximate


def print_subnet_info(interface: IPInterfaceT | IPNetworkT) -> None:
    """Print subnet information."""
    net = interface.network

    print(f"Details for IP Interface: {net.compressed}")
    print()

    print(f"    Prefix Size: /{net.prefixlen}")
    if interface.version == IP_VERSION_4:
        print(f"        Netmask: {net.netmask.compressed}")
        print(f"       Wildcard: {net.hostmask.compressed}")
    print()

    print(f"  First Address: {net[0].compressed}")
    print(f"   Last Address: {net[-1].compressed}")

    print(f"Total Addresses: {approximate(net.num_addresses)}")
