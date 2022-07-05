"""Functions for parsing various strings of interest."""
from __future__ import annotations

from typing import Iterable


def parsecmd(filename: str) -> list[str]:
    """Parses a file containing a command-line command."""
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


def parsemap(mapargs: Iterable[str]) -> dict[str, str]:
    """Parses an iterable of arguments into a directory mapping."""
    return dict(arg.split("::") for arg in mapargs)
