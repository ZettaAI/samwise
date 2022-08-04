"""Utility functions for working on google cloud."""
from __future__ import annotations

import subprocess

from . import parse


USERDATA_BASE = """#!/bin/bash
set -e
mount -t tmpfs -o size=80%,noatime tmpfs /tmp
DEBIAN_FRONTEND=noninteractive apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    dist-upgrade

echo ##### Set up Docker #############################################################
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository "deb [arch=amd64] \
    https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
apt-get update -y
apt-get install docker-ce -y
usermod -aG docker ubuntu
mkdir -p /etc/docker
systemctl restart docker
gcloud auth --quiet configure-docker


echo ##### Set up NVidia #############################################################
# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
        | tee /etc/apt/sources.list.d/nvidia-docker.list
add-apt-repository -y ppa:graphics-drivers/ppa
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install nvidia-headless-470 nvidia-container-toolkit nvidia-container-runtime
cat << EOF > /etc/docker/daemon.json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
EOF
systemctl restart docker

mkdir /workspace
"""


def cloud_init_file(dockerimage: str, commandfilename: str):
    """Returns file contents that tells a cloud instance how to start.

    Args:
        dockerimage: A docker image name.
        commandfilename: A path to a file where the command is stored.
    """
    command = parse.parsecmd(commandfilename)

    return (
        USERDATA_BASE
        + f"\ndocker run -v /workspace:/workspace {dockerimage} {' '.join(command)}"
    )


def create_instance(
    instancename: str,
    initfilename: str,
    zone: str = "us-east1-c",
    gpu: str = "nvidia-tesla-t4",
    gpu_count: int = 1,
    instancetype: str = "n1-standard-16",
    bootdisksize: str = "50GB",
    preemptible: bool = True,
    verbose: bool = True,
) -> None:
    """Creates an instance (currently just using gcloud).

    Args:
        instancename: how you'd like to name your instance.
        initfilename: a path to a file that tells your instance how to start.
        instancetype: the instance type (Default: "n1-standard-16")
        bootdisksize: how large of a boot disk you'd like (Default: "50GB")
        preemptible: whether you'd like your instance to be preemptible (Default: True)
    """
    args = [
        "gcloud",
        "compute",
        "instances",
        "create",
        instancename,
        f"--zone={zone}",
        "--image-family",
        "ubuntu-2204-lts",
        "--image-project",
        "ubuntu-os-cloud",
        "--metadata-from-file",
        f"user-data={initfilename}",
        "--machine-type",
        instancetype,
        f"--boot-disk-size={bootdisksize}",
        "--scopes=storage-rw",
    ]

    if preemptible:
        args.append("--preemptible")

    if not verbose:
        args.append("--quiet")

    if gpu is not None:
        args.append(f"--accelerator=type={gpu},count={gpu_count}")

    subprocess.run(args)
