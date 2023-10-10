"""General Utility Code."""


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
