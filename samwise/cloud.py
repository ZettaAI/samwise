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

    return USERDATA_BASE + f"\n{format_command(dockerimage, command)}"


def format_command(
    dockerimage: str, command: list[str], workspacedir: str = "/workspace"
) -> str:
    """Forms a complete docker run command from a container command."""
    if workspacedir is not None:
        return (
            "docker run"
            f" -v {workspacedir}:/workspace"
            f" -e PYTHONUNBUFFERED=1"
            f" --shm-size 1g"
            f" {dockerimage} {' '.join(command)}"
        )
    else:
        return (
            "docker run"
            f" -e PYTHONUNBUFFERED=1"
            f" --shm-size 1g"
            f" {dockerimage} {' '.join(command)}"
        )


def create_instance_group(
    groupname: str,
    initfilename: str,
    zone: str = "us-east1-c",
    gpu: str = "nvidia-tesla-t4",
    gpu_count: int = 1,
    instancetype: str = "n1-standard-16",
    bootdisksize: str = "50GB",
    preemptible: bool = True,
    verbose: bool = True,
) -> None:
    """Creates an instance group (currently just using gcloud).

    Args:
        instancename: how you'd like to name your instance.
        initfilename: a path to a file that tells your instance how to start.
        instancetype: the instance type (Default: "n1-standard-16")
        bootdisksize: how large of a boot disk you'd like (Default: "50GB")
        preemptible: whether you'd like your instance to be preemptible (Default: True)
    """
    template_args = [
        "gcloud",
        "compute",
        "instance-templates",
        "create",
        groupname,
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
        template_args.append("--preemptible")

    if not verbose:
        template_args.append("--quiet")

    if gpu is not None:
        template_args.append(f"--accelerator=type={gpu},count={gpu_count}")

    subprocess.check_call(template_args)

    group_args = [
        "gcloud",
        "compute",
        "instance-groups",
        "managed",
        "create",
        groupname,
        f"--zone={zone}",
        "--size=1",
        f"--template={groupname}",
    ]

    subprocess.check_call(group_args)
