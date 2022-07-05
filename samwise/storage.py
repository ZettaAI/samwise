"""Functions for managing files across storage systems."""
from __future__ import annotations

import os
import subprocess


def initdirs(dirmapping: dict[str, str]) -> None:
    """Initializes sync'd directories by downloading them from the remote version."""
    for remote, local in dirmapping.items():
        if not remotepath(local) and not os.path.exists(local):
            os.makedirs(local)
        subprocess.run(["gsutil", "-m", "rsync", "-r", remote, local], check=True)


def syncdirs(dirmapping: dict[str, str]) -> None:
    """Synchronizes any changes to the local directories with the remote ones."""
    for remote, local in dirmapping.items():
        subprocess.run(["gsutil", "-m", "rsync", "-r", local, remote], check=True)


def remotepath(path: str) -> bool:
    return path.startswith("gs://") or path.startswith("s3://")
