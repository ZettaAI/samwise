import time
import shutil

from samwise import run


def test_run(dummy_dir):
    def f():
        for i in range(2):
            time.sleep(1)
            print("still alive")
        print("dying")

    localdir = "test/dummy_dir_local"
    run(f, {dummy_dir: localdir}, period=2)

    shutil.rmtree(localdir)
