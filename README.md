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

### Subnet

The subnet command prints an IPv4 subnetting table, and by extension, converts
between various subnet specifiers (CIDR Prefix Length, Subnet Mask, and
Wildcard Mask).

If you provide a mask specifier as an argument only the related entry of the
table will be printed, which makes looking up the alternate specifiers easy.
Partial specifiers are allowed as well, and the command will do it's best to
identify which entry you need. For example, ".252" will assume a subnet mask
of "255.255.255.252" and show the details accordingly.

## Installation

    python3 -m pip install git+https://github.com/therealzanfar/iptool.git

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[zanfar/cookiecutter-pypackage](https://gitlab.com/zanfar/cookiecutter-pypackage)
project template.
