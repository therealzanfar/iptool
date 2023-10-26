# IP Tool

CLI Tools for Managing IP Addresses and Related Objects.

## Usage

The various iptool functions are broken down into separate "commands". To use
a specific function (or command) simply provide the name of the command
after the `iptool` invocation. For example, to run the "subnet" utility:

    iptool subnet

Each command has it's own help information, which can be viewed with the
`--help` option, and provides details on what arguments or options that
command accepts.

### Mask

The `mask` command prints an IPv4 subnetting table with the various masks for
each subnet size, and by extension, converts between various subnet specifiers
(CIDR Prefix Length, Subnet Mask, and Wildcard Mask).

If you provide a mask specifier as an argument, only the related entry of the
table will be printed, which makes looking up the alternate specifiers easy.
Partial specifiers are allowed as well, and the command will do it's best to
identify which entry you need. For example, ".252" will assume a subnet mask
of "255.255.255.252" and show the details accordingly.

The `mask` command is also the default command, and will be executed if no
command is provided.

The `mask` command has two shortcut aliases. Instead of `iptool mask`, the
following commands are also available:

-   `mask`
-   `cidr`

### Subnet

The `subnet` command provides details about a specified IP subnet. The command
requires both an address in the subnet and a mask specifier (CIDR Prefix
Length, Subnet Mask, or Wildcard Mask).

The details include:

-   First and last address
-   Network ID
-   Subnet size
-   Alternate mask specifiers (for IPv4)

The `subnet` command a shortcut aliase. Instead of `iptool subnet`, the
following command is also available:

-   `subnet`

## Installation

    python3 -m pip install git+https://github.com/therealzanfar/iptool.git

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[zanfar/cookiecutter-pypackage](https://gitlab.com/zanfar/cookiecutter-pypackage)
project template.
