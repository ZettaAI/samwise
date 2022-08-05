"""Main interface for running local commands."""
from __future__ import annotations

import argparse

from samwise import parse, runcmd


def run(
    commandfilename: str,
    dirmapping: dict[str, str],
    period: int = 600,
    verbose: bool = True,
) -> None:

    args = parse.parsecmd(commandfilename)

    runcmd(args, dirmapping, period=period, verbose=verbose)


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("commandfilename", type=str, help="The command line to run")
    ap.add_argument(
        "dirmapping",
        type=str,
        nargs="+",
        help=(
            'The directories to map split by "::"s.'
            " e.g., remote1::local1 remote2::local2"
        ),
    )
    ap.add_argument(
        "--period",
        type=int,
        default=600,
        help="How often to synchronize directories (in seconds). Default=600",
    )
    ap.add_argument(
        "--quiet", dest="verbose", action="store_false", help="Produce less output"
    )

    args = ap.parse_args()

    args.dirmapping = dict(arg.split("::") for arg in args.dirmapping)

    run(**vars(args))
