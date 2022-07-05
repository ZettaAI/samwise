import os
import shutil
from pathlib import Path

from samwise import storage


def all_contained(ref, dest):
    contents = os.listdir(ref)

    for f in contents:
        testpath = os.path.join(dest, f)
        if not os.path.exists(testpath):
            return False

    return True


def test_initdirs(dummy_dir):

    local = f"{dummy_dir}_local"

    storage.initdirs({dummy_dir: local})

    assert all_contained(dummy_dir, local)

    shutil.rmtree(local)


def test_syncdirs(dummy_dir):

    local = f"{dummy_dir}_local"
    dirmapping = {dummy_dir: local}

    storage.initdirs(dirmapping)
    Path(os.path.join(local, "d")).touch()

    storage.syncdirs(dirmapping)

    assert all_contained(local, dummy_dir)

    shutil.rmtree(local)
