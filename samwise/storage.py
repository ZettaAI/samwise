"""Functions for managing files across storage systems."""
from __future__ import annotations

import os
import subprocess


def initdirs(dirmapping: dict[str, str], verbose: bool = True) -> None:
    """Initializes sync'd directories by downloading them from the remote version."""
    for remote, local in dirmapping.items():
        if not remotepath(local) and not os.path.exists(local):
            os.makedirs(local)

        if verbose:
            subprocess.run(["gsutil", "-m", "rsync", "-r", remote, local], check=True)
        else:
            subprocess.run(["gsutil", "-mq", "rsync", "-r", remote, local], check=True)


def syncdirs(dirmapping: dict[str, str], verbose: bool = True) -> None:
    """Synchronizes any changes to the local directories with the remote ones."""
    for remote, local in dirmapping.items():
        if verbose:
            subprocess.run(["gsutil", "-m", "rsync", "-r", local, remote], check=True)
        else:
            subprocess.run(["gsutil", "-mq", "rsync", "-r", local, remote], check=True)


def remotepath(path: str) -> bool:
    """Checks whether a path points to cloud storage."""
    return path.startswith("gs://") or path.startswith("s3://")
