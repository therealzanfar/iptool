"""Test the iptool Subnet Utility."""

import pytest

from iptool.subnet import (
    _parse_ipv4_cidr_masklen,
    _parse_ipv4_subnet_mask,
    _parse_ipv4_wildcard_mask,
    parse_subnet_fragment,
)

PARAMS_MASKLENS = [
    # fmt: off
    pytest.param(r"0",    0, id="0"  ),
    pytest.param(r"1",    1, id="1"  ),
    pytest.param(r"2",    2, id="2"  ),
    pytest.param(r"3",    3, id="3"  ),
    pytest.param(r"4",    4, id="4"  ),
    pytest.param(r"5",    5, id="5"  ),
    pytest.param(r"6",    6, id="6"  ),
    pytest.param(r"7",    7, id="7"  ),
    pytest.param(r"8",    8, id="8"  ),
    pytest.param(r"9",    9, id="9"  ),
    pytest.param(r"10",  10, id="10" ),
    pytest.param(r"11",  11, id="11" ),
    pytest.param(r"12",  12, id="12" ),
    pytest.param(r"13",  13, id="13" ),
    pytest.param(r"14",  14, id="14" ),
    pytest.param(r"15",  15, id="15" ),
    pytest.param(r"16",  16, id="16" ),
    pytest.param(r"17",  17, id="17" ),
    pytest.param(r"18",  18, id="18" ),
    pytest.param(r"19",  19, id="19" ),
    pytest.param(r"20",  20, id="20" ),
    pytest.param(r"21",  21, id="21" ),
    pytest.param(r"22",  22, id="22" ),
    pytest.param(r"23",  23, id="23" ),
    pytest.param(r"24",  24, id="24" ),
    pytest.param(r"25",  25, id="25" ),
    pytest.param(r"26",  26, id="26" ),
    pytest.param(r"27",  27, id="27" ),
    pytest.param(r"28",  28, id="28" ),
    pytest.param(r"29",  29, id="29" ),
    pytest.param(r"30",  30, id="30" ),
    pytest.param(r"31",  31, id="31" ),
    pytest.param(r"32",  32, id="32" ),

    pytest.param(r"/0",   0, id="/0" ),
    pytest.param(r"/1",   1, id="/1" ),
    pytest.param(r"/2",   2, id="/2" ),
    pytest.param(r"/3",   3, id="/3" ),
    pytest.param(r"/4",   4, id="/4" ),
    pytest.param(r"/5",   5, id="/5" ),
    pytest.param(r"/6",   6, id="/6" ),
    pytest.param(r"/7",   7, id="/7" ),
    pytest.param(r"/8",   8, id="/8" ),
    pytest.param(r"/9",   9, id="/9" ),
    pytest.param(r"/10", 10, id="/10"),
    pytest.param(r"/11", 11, id="/11"),
    pytest.param(r"/12", 12, id="/12"),
    pytest.param(r"/13", 13, id="/13"),
    pytest.param(r"/14", 14, id="/14"),
    pytest.param(r"/15", 15, id="/15"),
    pytest.param(r"/16", 16, id="/16"),
    pytest.param(r"/17", 17, id="/17"),
    pytest.param(r"/18", 18, id="/18"),
    pytest.param(r"/19", 19, id="/19"),
    pytest.param(r"/20", 20, id="/20"),
    pytest.param(r"/21", 21, id="/21"),
    pytest.param(r"/22", 22, id="/22"),
    pytest.param(r"/23", 23, id="/23"),
    pytest.param(r"/24", 24, id="/24"),
    pytest.param(r"/25", 25, id="/25"),
    pytest.param(r"/26", 26, id="/26"),
    pytest.param(r"/27", 27, id="/27"),
    pytest.param(r"/28", 28, id="/28"),
    pytest.param(r"/29", 29, id="/29"),
    pytest.param(r"/30", 30, id="/30"),
    pytest.param(r"/31", 31, id="/31"),
    pytest.param(r"/32", 32, id="/32"),
    # fmt: on
]

PARAMS_SUBNETS = [
    # fmt: off

    ### Full Subnets

    pytest.param(r"255.255.255.255", 32, id="255.255.255.255"),
    pytest.param(r"255.255.255.254", 31, id="255.255.255.254"),
    pytest.param(r"255.255.255.252", 30, id="255.255.255.252"),
    pytest.param(r"255.255.255.248", 29, id="255.255.255.248"),
    pytest.param(r"255.255.255.240", 28, id="255.255.255.240"),
    pytest.param(r"255.255.255.224", 27, id="255.255.255.224"),
    pytest.param(r"255.255.255.192", 26, id="255.255.255.192"),
    pytest.param(r"255.255.255.128", 25, id="255.255.255.128"),

    pytest.param(r"255.255.255.0",   24, id="255.255.255.0"  ),
    pytest.param(r"255.255.254.0",   23, id="255.255.254.0"  ),
    pytest.param(r"255.255.252.0",   22, id="255.255.252.0"  ),
    pytest.param(r"255.255.248.0",   21, id="255.255.248.0"  ),
    pytest.param(r"255.255.240.0",   20, id="255.255.240.0"  ),
    pytest.param(r"255.255.224.0",   19, id="255.255.224.0"  ),
    pytest.param(r"255.255.192.0",   18, id="255.255.192.0"  ),
    pytest.param(r"255.255.128.0",   17, id="255.255.128.0"  ),

    pytest.param(r"255.255.0.0",     16, id="255.255.0.0"    ),
    pytest.param(r"255.254.0.0",     15, id="255.254.0.0"    ),
    pytest.param(r"255.252.0.0",     14, id="255.252.0.0"    ),
    pytest.param(r"255.248.0.0",     13, id="255.248.0.0"    ),
    pytest.param(r"255.240.0.0",     12, id="255.240.0.0"    ),
    pytest.param(r"255.224.0.0",     11, id="255.224.0.0"    ),
    pytest.param(r"255.192.0.0",     10, id="255.192.0.0"    ),
    pytest.param(r"255.128.0.0",      9, id="255.128.0.0"    ),

    pytest.param(r"255.0.0.0",        8, id="255.0.0.0"      ),
    pytest.param(r"254.0.0.0",        7, id="254.0.0.0"      ),
    pytest.param(r"252.0.0.0",        6, id="252.0.0.0"      ),
    pytest.param(r"248.0.0.0",        5, id="248.0.0.0"      ),
    pytest.param(r"240.0.0.0",        4, id="240.0.0.0"      ),
    pytest.param(r"224.0.0.0",        3, id="224.0.0.0"      ),
    pytest.param(r"192.0.0.0",        2, id="192.0.0.0"      ),
    pytest.param(r"128.0.0.0",        1, id="128.0.0.0"      ),

    pytest.param(r"0.0.0.0",          0, id="0.0.0.0"        ),


    ### Shorthand Subnets

    pytest.param(r".255",            32, id=".255"           ),

    pytest.param(r".254",            31, id=".254"           ),
    pytest.param(r".252",            30, id=".252"           ),
    pytest.param(r".248",            29, id=".248"           ),
    pytest.param(r".240",            28, id=".240"           ),
    pytest.param(r".224",            27, id=".224"           ),
    pytest.param(r".192",            26, id=".192"           ),
    pytest.param(r".128",            25, id=".128"           ),
    pytest.param(r".0",              24, id=".0"             ),

    pytest.param(r".254.0",          23, id=".254.0"         ),
    pytest.param(r".252.0",          22, id=".252.0"         ),
    pytest.param(r".248.0",          21, id=".248.0"         ),
    pytest.param(r".240.0",          20, id=".240.0"         ),
    pytest.param(r".224.0",          19, id=".224.0"         ),
    pytest.param(r".192.0",          18, id=".192.0"         ),
    pytest.param(r".128.0",          17, id=".128.0"         ),
    pytest.param(r".0.0",            16, id=".0.0"           ),

    pytest.param(r".254.0.0",        15, id=".254.0.0"       ),
    pytest.param(r".252.0.0",        14, id=".252.0.0"       ),
    pytest.param(r".248.0.0",        13, id=".248.0.0"       ),
    pytest.param(r".240.0.0",        12, id=".240.0.0"       ),
    pytest.param(r".224.0.0",        11, id=".224.0.0"       ),
    pytest.param(r".192.0.0",        10, id=".192.0.0"       ),
    pytest.param(r".128.0.0",         9, id=".128.0.0"       ),
    pytest.param(r".0.0.0",           8, id=".0.0.0"         ),
    # fmt: on
]

PARAMS_WILDCARDS = [
    # fmt: off

    ### Full Wildcards

    # 0.0.0.0 is assumed to be a subnet mask, not a wildcard mask
    pytest.param(r"0.0.0.1",         31, id="0.0.0.1"        ),
    pytest.param(r"0.0.0.3",         30, id="0.0.0.3"        ),
    pytest.param(r"0.0.0.7",         29, id="0.0.0.7"        ),
    pytest.param(r"0.0.0.15",        28, id="0.0.0.15"       ),
    pytest.param(r"0.0.0.31",        27, id="0.0.0.31"       ),
    pytest.param(r"0.0.0.63",        26, id="0.0.0.63"       ),
    pytest.param(r"0.0.0.127",       25, id="0.0.0.127"      ),

    pytest.param(r"0.0.0.255",       24, id="0.0.0.255"      ),
    pytest.param(r"0.0.1.255",       23, id="0.0.1.255"      ),
    pytest.param(r"0.0.3.255",       22, id="0.0.3.255"      ),
    pytest.param(r"0.0.7.255",       21, id="0.0.7.255"      ),
    pytest.param(r"0.0.15.255",      20, id="0.0.15.255"     ),
    pytest.param(r"0.0.31.255",      19, id="0.0.31.255"     ),
    pytest.param(r"0.0.63.255",      18, id="0.0.63.255"     ),
    pytest.param(r"0.0.127.255",     17, id="0.0.127.255"    ),

    pytest.param(r"0.0.255.255",     16, id="0.0.255.255"    ),
    pytest.param(r"0.1.255.255",     15, id="0.1.255.255"    ),
    pytest.param(r"0.3.255.255",     14, id="0.3.255.255"    ),
    pytest.param(r"0.7.255.255",     13, id="0.7.255.255"    ),
    pytest.param(r"0.15.255.255",    12, id="0.15.255.255"   ),
    pytest.param(r"0.31.255.255",    11, id="0.31.255.255"   ),
    pytest.param(r"0.63.255.255",    10, id="0.63.255.255"   ),
    pytest.param(r"0.127.255.255",    9, id="0.127.255.255"  ),

    pytest.param(r"0.255.255.255",    8, id="0.127.255.255"  ),
    pytest.param(r"1.255.255.255",    7, id="1.255.255.255"  ),
    pytest.param(r"3.255.255.255",    6, id="3.255.255.255"  ),
    pytest.param(r"7.255.255.255",    5, id="7.255.255.255"  ),
    pytest.param(r"15.255.255.255",   4, id="15.255.255.255" ),
    pytest.param(r"31.255.255.255",   3, id="31.255.255.255" ),
    pytest.param(r"63.255.255.255",   2, id="63.255.255.255" ),
    pytest.param(r"127.255.255.255",  1, id="127.255.255.255"),
    # 255.255.255.255 is assumed to be a subnet mask, not a wildcard mask


    ### Shortcut Wildcards

    # .0 is assumed to be a subnet mask, not a wildcard mask
    pytest.param(r".1",              31, id=".1"             ),
    pytest.param(r".3",              30, id=".3"             ),
    pytest.param(r".7",              29, id=".7"             ),
    pytest.param(r".15",             28, id=".15"            ),
    pytest.param(r".31",             27, id=".31"            ),
    pytest.param(r".63",             26, id=".63"            ),
    pytest.param(r".127",            25, id=".127"           ),
    # .255 is assumed to be a subnet mask, not a wildcard mask

    pytest.param(r".1.255",          23, id=".1.255"         ),
    pytest.param(r".3.255",          22, id=".3.255"         ),
    pytest.param(r".7.255",          21, id=".7.255"         ),
    pytest.param(r".15.255",         20, id=".15.255"        ),
    pytest.param(r".31.255",         19, id=".31.255"        ),
    pytest.param(r".63.255",         18, id=".63.255"        ),
    pytest.param(r".127.255",        17, id=".127.255"       ),
    pytest.param(r".255.255",        16, id=".127.255"       ),

    pytest.param(r".1.255.255",      15, id=".1.255.255"     ),
    pytest.param(r".3.255.255",      14, id=".3.255.255"     ),
    pytest.param(r".7.255.255",      13, id=".7.255.255"     ),
    pytest.param(r".15.255.255",     12, id=".15.255.255"    ),
    pytest.param(r".31.255.255",     11, id=".31.255.255"    ),
    pytest.param(r".63.255.255",     10, id=".63.255.255"    ),
    pytest.param(r".127.255.255",     9, id=".127.255.255"   ),
    pytest.param(r".255.255.255",     8, id=".127.255.255"   ),
    # fmt: on
]


@pytest.mark.parametrize(
    ("fragment", "expected"),
    PARAMS_MASKLENS,
)
def test_masklength_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_cidr_masklen(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    PARAMS_SUBNETS,
)
def test_subnet_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_subnet_mask(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    PARAMS_WILDCARDS,
)
def test_wildcard_parse(fragment: str, expected: int) -> None:
    assert _parse_ipv4_wildcard_mask(fragment) == expected


@pytest.mark.parametrize(
    ("fragment", "expected"),
    PARAMS_MASKLENS + PARAMS_SUBNETS + PARAMS_WILDCARDS,
)
def test_fragment_parse(fragment: str, expected: int) -> None:
    assert parse_subnet_fragment(fragment) == expected
