"""Tests for the task generation scripts."""
import tempfile
import subprocess


def test_flap():
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write("")
        tmp.flush()

        subprocess.check_call(["samwise-flap", tmp.name, "hello-world", "--nosudo"])
