"""Tests for the task generation scripts."""
import tempfile
import subprocess


# Helper functions
def check_cmd(filename: str, *args: str) -> None:
    """Runs a script within a subprocess to make sure that argparsing works."""
    subprocess.check_call(["python", filename, *args])


# Actual tests
def test_flap():
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write("")
        tmp.flush()

        check_cmd("scripts/flap.py", tmp.name, "hello-world", "--nosudo")
