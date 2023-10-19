"""Network Subnet Related Code."""

from iptool.cli import rprint
from iptool.ip import IP_VERSION_4, IPInterfaceT, IPNetworkT
from iptool.utils import approximate


def print_subnet_info(interface: IPInterfaceT | IPNetworkT) -> None:
    """Print subnet information."""
    net = interface.network

    rprint(
        "[bold underline]"
        f"Details for IP Interface: [ip]{interface.compressed}[/ip]"
        "[/bold underline]",
    )
    rprint()

    rprint(f"    Prefix Size: [masklen]/{net.prefixlen}[/masklen]")
    if interface.version == IP_VERSION_4:
        rprint(f"        Netmask: [netmask]{net.netmask.compressed}[/netmask]")
        rprint(f"       Wildcard: [hostmask]{net.hostmask.compressed}[/hostmask]")
    rprint()

    rprint(f"  First Address: [ip]{net[0].compressed}[/ip]")
    rprint(f"   Last Address: [ip]{net[-1].compressed}[/ip]")

    rprint(f"Total Addresses: [number]{approximate(net.num_addresses)}[/number]")
