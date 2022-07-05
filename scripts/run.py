"""Main interface for running local commands."""
import argparse

from samwise import parse, run


def main(
    commandfilename: str,
    dirmapping: dict[str, str],
    period: int = 600,
    verbose: bool = True,
) -> None:

    args = parse.parsecmd(commandfilename)

    run.runcmd(args, dirmapping, period=period, verbose=verbose)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("commandfilename", type=str)
    ap.add_argument("dirmapping", type=str, nargs="+")
    ap.add_argument("--period", type=int, default=600)
    ap.add_argument("--quiet", dest="verbose", action="store_false")

    args = ap.parse_args()

    args.dirmapping = dict(arg.split("::") for arg in args.dirmapping)

    main(**vars(args))
