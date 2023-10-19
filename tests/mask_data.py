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


class MaskTestDataItemT(TypedDict):  # noqa: D101
    input: str
    expected: int


class MaskTestDataT(TypedDict):  # noqa: D101
    masklens: list[MaskTestDataItemT]
    netmasks: list[MaskTestDataItemT]
    hostmasks: list[MaskTestDataItemT]


mask_test_data: MaskTestDataT

mask_test_data_path = Path(__file__).resolve().parent / "mask_data.json"
with open(mask_test_data_path, encoding="utf-8") as data_fh:
    mask_test_data = cast(MaskTestDataT, json.load(data_fh))


MASKLEN_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in mask_test_data["masklens"]
]

NETMASK_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in mask_test_data["netmasks"]
]

HOSTMASK_TEST_DATA = [
    pytest.param(
        item["input"],
        item["expected"],
        id=item["input"],
    )
    for item in mask_test_data["hostmasks"]
]
