import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def dummy_dir():
    dirname = "test/dummy_dir"
    os.makedirs(dirname, exist_ok=True)

    for filename in ["a", "b", "c"]:
        Path(os.path.join(dirname, filename)).touch()

    yield dirname

    shutil.rmtree(dirname)
