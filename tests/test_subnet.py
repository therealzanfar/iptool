"""Test the iptool Subnet Utility."""

from io import StringIO
from typing import NamedTuple
from unittest.mock import patch

import pytest

from iptool.subnet import (
    _parse_ipv4_cidr_masklen,
    _parse_ipv4_subnet_mask,
    _parse_ipv4_wildcard_mask,
    parse_subnet_fragment,
    print_ipv4_subnet_table,
)

from .subnet_data import HOSTMASK_TEST_DATA, MASKLEN_TEST_DATA, NETMASK_TEST_DATA


@pytest.mark.parametrize(
    ("fragment", "expected"),
    MASKLEN_TEST_DATA,
)
def test_masklength_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_cidr_masklen(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    NETMASK_TEST_DATA,
)
def test_subnet_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_subnet_mask(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    HOSTMASK_TEST_DATA,
)
def test_wildcard_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_wildcard_mask(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    MASKLEN_TEST_DATA + NETMASK_TEST_DATA + HOSTMASK_TEST_DATA,
)
def test_fragment_parse(fragment: str, expected: int) -> None:
    assert parse_subnet_fragment(fragment) == expected


class ExpectedSubnetInfoT(NamedTuple):  # noqa: D101
    masklen: str
    netmask: str
    hostmask: str


@patch("sys.stdout", new_callable=StringIO)
@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [
        pytest.param(1, 1, [ExpectedSubnetInfoT("/1", "128.0.0.0", "127.255.255.255")]),
        pytest.param(
            24,
            24,
            [ExpectedSubnetInfoT("/24", "255.255.255.0", "0.0.0.255")],
        ),
        pytest.param(
            31,
            31,
            [ExpectedSubnetInfoT("/31", "255.255.255.254", "0.0.0.1")],
        ),
        pytest.param(
            1,
            24,
            [
                ExpectedSubnetInfoT("/1", "128.0.0.0", "127.255.255.255"),
                ExpectedSubnetInfoT("/24", "255.255.255.0", "0.0.0.255"),
            ],
        ),
        pytest.param(
            24,
            31,
            [
                ExpectedSubnetInfoT("/24", "255.255.255.0", "0.0.0.255"),
                ExpectedSubnetInfoT("/31", "255.255.255.254", "0.0.0.1"),
            ],
        ),
    ],
)
def test_ipv4_table(
    mock_stdout: StringIO,
    start: int,
    end: int,
    expected: list[ExpectedSubnetInfoT],
) -> None:
    print_ipv4_subnet_table(start, end)
    output = mock_stdout.getvalue()

    for exp in expected:
        assert exp.masklen in output
        assert exp.netmask in output
        assert exp.hostmask in output
