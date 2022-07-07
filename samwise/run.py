"""Running functionality while periodically synchronizing directories elsewhere."""
from __future__ import annotations

import time
import subprocess
from typing import Callable
from threading import Thread
from datetime import datetime

from . import storage


def runcmd(
    args: list[str],
    dirmapping: dict[str, str],
    period: int = 600,
    verbose: bool = True,
) -> None:
    # Make a partial fn that runs the command in a subprocess

    def startprocess():
        subprocess.run(args)

    run(startprocess, dirmapping, period=period, verbose=verbose)


def run(
    f: Callable,
    dirmapping: dict[str, str],
    period: int = 600,
    verbose: bool = True,
) -> None:

    if verbose:
        print("INITIALIZING SYNCHRONIZATION")
    storage.initdirs(dirmapping, verbose=verbose)

    if verbose:
        printmsg("STARTING MAIN THREAD")

    t = Thread(target=f)
    t.start()

    start = datetime.now()
    i = 0
    while True:
        time.sleep(1)

        if not t.is_alive():
            storage.syncdirs(dirmapping, verbose=verbose)
            break

        elapsed = datetime.now() - start
        if elapsed.total_seconds() // period > i:

            if verbose:
                printmsg("STARTING SYNCHRONIZATION")

            storage.syncdirs(dirmapping, verbose=verbose)

            i += 1


def printmsg(msg: str) -> None:
    print(f"=========={msg}==========")
