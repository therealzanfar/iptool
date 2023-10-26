"""Test the `iptool` Subnet Utility CLI."""
import pytest
from click.testing import CliRunner

from iptool.__main__ import cli_main
from iptool.mask.__main__ import cli_mask

from .mask_data import HOSTMASK_TEST_DATA, MASKLEN_TEST_DATA, NETMASK_TEST_DATA


@pytest.mark.parametrize(
    ("fragment", "expected"),
    [
        HOSTMASK_TEST_DATA[0],
        HOSTMASK_TEST_DATA[-1],
        MASKLEN_TEST_DATA[0],
        MASKLEN_TEST_DATA[-1],
        NETMASK_TEST_DATA[0],
        NETMASK_TEST_DATA[-1],
    ],
)
def test_subnet_cli_click_fragment(fragment: str, expected: int) -> None:
    runner = CliRunner()
    cidr = f"/{expected}"

    main_result = runner.invoke(cli_main, [fragment])
    assert cidr in main_result.output

    command_result = runner.invoke(cli_mask, [fragment])
    assert cidr in command_result.output


def test_subnet_cli_click_default() -> None:
    runner = CliRunner()

    main_result = runner.invoke(cli_main)
    assert "/20" in main_result.output
    assert "/24" in main_result.output
    assert "/31" in main_result.output

    command_result = runner.invoke(cli_mask)
    assert "/20" in command_result.output
    assert "/24" in command_result.output
    assert "/31" in command_result.output


def test_subnet_cli_click_all() -> None:
    runner = CliRunner()

    main_result = runner.invoke(cli_main, ["--show-all"])
    assert "/1" in main_result.output
    assert "/32" in main_result.output

    main_short_result = runner.invoke(cli_main, ["-a"])
    assert "/1" in main_short_result.output
    assert "/32" in main_short_result.output

    command_result = runner.invoke(cli_mask, ["--show-all"])
    assert "/1" in command_result.output
    assert "/32" in command_result.output

    command_short_result = runner.invoke(cli_mask, ["-a"])
    assert "/1" in command_short_result.output
    assert "/32" in command_short_result.output
