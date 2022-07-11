"""Creates an instance to run a preemptible command in the cloud."""
import argparse
import tempfile

from samwise import cloud


def fly(
    commandfilename: str,
    dockerimage: str,
    instancetype: str,
    zone: str = "us-east1-c",
    gpu: str = "nvidia-tesla-t4",
    gpu_count: int = 1,
    instancename: str = "n1-standard-16",
    bootdisksize: str = "50GB",
    preemptible: bool = True,
    verbose: bool = True,
) -> None:
    """Creates an instance that runs a command in a specified docker container."""
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(cloud.cloud_init_file(dockerimage, commandfilename))
        tmp.flush()
        cloud.create_instance(
            instancename,
            tmp.name,
            zone=zone,
            gpu=gpu,
            gpu_count=gpu_count,
            instancetype=instancetype,
            bootdisksize=bootdisksize,
            preemptible=preemptible,
            verbose=verbose,
        )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("commandfilename")
    ap.add_argument("dockerimage")
    ap.add_argument("instancename")
    ap.add_argument("--zone", default="us-east1-c")
    ap.add_argument("--gpu", default="nvidia-tesla-t4")
    ap.add_argument("--gpu-count", type=int, default=1)
    ap.add_argument("--instancetype", default="n1-standard-16")
    ap.add_argument("--quiet", dest="verbose", action="store_false")
    ap.add_argument("--bootdisksize", type=str, default="50GB")
    ap.add_argument("--not-preemptible", dest="preemptible", action="store_false")

    fly(**vars(ap.parse_args()))
