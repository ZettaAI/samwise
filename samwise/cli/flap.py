"""Runs a commandfile locally.

Useful for testing command files before sending them to remote instances with fly.
"""
from __future__ import annotations

import os
import argparse
import subprocess

from samwise import parse, cloud


def flap(
    commandfilename: str,
    dockerimage: str,
    workspacedir: str,
    sudo: bool = True,
) -> None:
    """Tests a commandfile by running it locally."""
    if workspacedir is not None:
        os.makedirs(workspacedir, exist_ok=True)

    rawcommand = parse.parsecmd(commandfilename)
    formatted = cloud.format_command(dockerimage, rawcommand, workspacedir).split()

    if sudo:
        subprocess.run(["sudo"] + formatted)
    else:
        subprocess.run(formatted)


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "commandfilename",
        type=str,
        help="A file containing the command or arguments for your docker container",
    )
    ap.add_argument("dockerimage", type=str, help="The name of your docker image")
    ap.add_argument(
        "--workspacedir",
        type=str,
        default=None,
        help="A directory to mount as the workspace",
    )
    ap.add_argument(
        "--nosudo", action="store_false", dest="sudo", help="Don't run docker with sudo"
    )

    flap(**vars(ap.parse_args()))
