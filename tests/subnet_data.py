"""Subnet-Related Test Data."""

import json
from pathlib import Path
from typing import TypedDict, cast

import pytest

__ALL__ = [
    "MASKLEN_TEST_DATA",
    "NETMASK_TEST_DATA",
    "HOSTMASK_TEST_DATA",
]


class SubnetTestDataItemT(TypedDict):  # noqa: D101
    input: str
    expected: int


class SubnetTestDataT(TypedDict):  # noqa: D101
    masklens: list[SubnetTestDataItemT]
    netmasks: list[SubnetTestDataItemT]
    hostmasks: list[SubnetTestDataItemT]


subnet_test_data: SubnetTestDataT

subnet_test_data_path = Path(__file__).resolve().parent / "subnet_data.json"
with open(subnet_test_data_path, encoding="utf-8") as data_fh:
    subnet_test_data = cast(SubnetTestDataT, json.load(data_fh))


MASKLEN_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in subnet_test_data["masklens"]
]

NETMASK_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in subnet_test_data["netmasks"]
]

HOSTMASK_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in subnet_test_data["hostmasks"]
]
