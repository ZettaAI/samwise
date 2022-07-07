"""Functions for parsing various strings of interest."""
from __future__ import annotations

from typing import Iterable


def parsecmd(filename: str) -> list[str]:
    """Parses a file containing a command-line command.

    Args:
        filename: A path to the input file.
    Returns:
        A list of shell arguments
    """
    with open(filename) as f:
        lines = f.readlines()

    cleaned = [
        line.replace("\\\n", "").replace("\n", "").replace("\\", "") for line in lines
    ]

    args = list()
    for line in cleaned:
        for arg in line.split():
            if arg != "":
                args.append(arg)

    return args


def parsemap(mapargs: Iterable[str], sep="::") -> dict[str, str]:
    """Parses an iterable of arguments into a directory mapping.

    Args:
        mapargs: A set of arguments splitting map items by a separator
        sep: The separator to use when splitting the arguments. Default ::
    Returns:
        A dictionary containing each of the map items.
    """
    return dict(arg.split(sep) for arg in mapargs)
