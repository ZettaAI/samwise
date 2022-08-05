"""Creates an instance to run a preemptible command in the cloud."""
from __future__ import annotations

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


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "commandfilename",
        type=str,
        help="A file containing the command or arguments for your docker container",
    )
    ap.add_argument("dockerimage", type=str, help="The name of your docker image")
    ap.add_argument(
        "instancename",
        type=str,
        help="A name for the instance running this docker container",
    )
    ap.add_argument(
        "--zone",
        type=str,
        help='The gcp zone for this instance. Default="us-east1-c"',
        default="us-east1-c",
    )
    ap.add_argument(
        "--gpu",
        type=str,
        help='The type of GPU to use if desired. Default="nvidia-tesla-t4"',
        default="nvidia-tesla-t4",
    )
    ap.add_argument(
        "--gpu-count",
        type=int,
        help="How many gpus to attach to your instance. Default=1",
        default=1,
    )
    ap.add_argument(
        "--instancetype",
        type=str,
        help='The instance type to use. Default="n1-standard-16""',
        default="n1-standard-16",
    )
    ap.add_argument(
        "--quiet", action="store_false", dest="verbose", help="Produce less output"
    )
    ap.add_argument(
        "--bootdisksize",
        type=str,
        help='How large to make your instance\'s boot disk. Default="50GB"',
        default="50GB",
    )
    ap.add_argument(
        "--not-preemptible",
        action="store_false",
        dest="preemptible",
        help="Don't use a preemptible instance",
    )

    fly(**vars(ap.parse_args()))
