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
    """Runs a shell command while synchronizing directories.

    Args:
        args: Shell command and its arguments
        dirmapping: A dictionary from remote to local storage for synchronization
        period: How often (in seconds) to synchronize the stored files
        verbose: Whether or not to print messages when synchronization takes place
    """
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
    """Runs a callable while synchronizing directories.

    Args:
        f: A python callable of some kind (function, partial, etc.)
        dirmapping: A dictionary from remote to local storage for synchronization
        period: How often (in seconds) to synchronize the stored files
        verbose: Whether or not to print messages when synchronization takes place
    """

    if verbose:
        print("INITIALIZING SYNCHRONIZATION")
    storage.initdirs(dirmapping, verbose=verbose)

    if verbose:
        printmsg("STARTING SYNC THREAD")

    t = Thread(
        target=syncthread,
        args=(dirmapping,),
        kwargs=dict(period=period, verbose=verbose),
    )
    t.daemon = True
    t.start()

    f()


def syncthread(
    dirmapping: dict[str, str], period: int = 600, verbose: bool = True
) -> None:
    start = datetime.now()
    i = 0
    while True:
        time.sleep(1)

        elapsed = datetime.now() - start
        if elapsed.total_seconds() // period > i:

            if verbose:
                printmsg("STARTING SYNCHRONIZATION")

            try:
                storage.syncdirs(dirmapping, verbose=verbose)
            except Exception as e:
                print(e)
                i -= 1  # retrying after the sleep

            i += 1


def printmsg(msg: str) -> None:
    print(f"=========={msg}==========")
