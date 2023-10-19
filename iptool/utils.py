"""General Utility Code."""

from typing import NamedTuple


class SIPrefix(NamedTuple):  # noqa: D101
    symbol: str
    name: str
    binary_name: str = ""
    imperial_name: str = ""

    @property
    def binary(self) -> str:  # noqa: D102
        return self.binary_name or self.name

    @property
    def imperial(self) -> str:  # noqa: D102
        return self.imperial_name or self.name


PREFIXES: dict[int, SIPrefix] = {
    0: SIPrefix("", "", "", ""),
    3: SIPrefix("k", "Kilo", "Kibi", "Thousand"),
    6: SIPrefix("M", "Mega", "mibi", "Million"),
    9: SIPrefix("G", "Giga", "Gibi", "Billion"),
    12: SIPrefix("T", "Tera", "Tebi", "Trillion"),
    15: SIPrefix("P", "Peta", "Pebi", "Quadrillion"),
    18: SIPrefix("E", "Exa", "Exbi", "Quintillion"),
}


def ordinal(num: int) -> str:
    """Convert an integer to an ordinal."""
    unit = num % 10

    suffix = "th"
    if unit == 1:
        suffix = "st"
    elif unit == 2:  # noqa: PLR2004
        suffix = "nd"
    elif unit == 3:  # noqa: PLR2004
        suffix = "rd"

    return f"{num}{suffix}"


def approximate(num: int, binary: bool = False) -> str:
    """Generate an approximate representation of an integer."""
    mag = 1000 if not binary else 1024
    neg = "-" if num < 0 else ""

    if num < mag:
        return str(num)

    num = abs(num)
    exp = 0

    while num > mag:
        num /= mag
        exp += 3

    if exp in PREFIXES:
        return f"≈ {neg}{num:.1f} {PREFIXES[exp].imperial}"

    return None
