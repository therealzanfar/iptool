"""Console Utilities for iptool Utility."""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

CLICK_CONTEXT = {"help_option_names": ["-h", "--help"]}

RICH_THEME = Theme(
    {
        "ip": "bold blue",
        "masklen": "bold magenta",
        "netmask": "bold green",
        "hostmask": "bold yellow",
        "number": "bold bright_white",
    },
    inherit=False,
)

rprint = Console(theme=RICH_THEME).print


def setup_logging(verbosity: int = 0) -> None:
    """
    Set up a root logger with console output.

    Args:
        verbosity (int, optional): The logging level; 0=Error, 1=Warning,
            2=Info, 3+=Debug. Defaults to 0.
    """
    logging_level = logging.ERROR
    if verbosity == 1:
        logging_level = logging.WARNING
    elif verbosity == 2:  # noqa: PLR2004
        logging_level = logging.INFO
    elif verbosity >= 3:  # noqa: PLR2004
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format="%(message)s",
        datefmt="[%x]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
