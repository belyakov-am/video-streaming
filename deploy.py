import os
import pathlib

from pssh.clients import ParallelSSHClient
from pssh.output import HostOutput
from typing import List

PARENT_DIR = pathlib.Path(__file__).parent.absolute()

PUBLIC_NGINX_IP = "130.193.48.177"
HOSTS = [
    "192.168.0.29",
]


def log_outputs(outputs: List[HostOutput]) -> None:
    for output in outputs:
        print(f'{output.host}:')
        print('Output:')
        for line in output.stdout:
            print(line)

        print('Error:')
        for line in output.stderr:
            print(line)


def main() -> None:
    client = ParallelSSHClient(
        hosts=HOSTS,
        pkey='~/.ssh/id_rsa',
        proxy_host=PUBLIC_NGINX_IP,
        user="ubuntu",
    )

    # Copy project files
    copy_dir_outputs = client.copy_file(
        local_file=f"{PARENT_DIR}/src",
        remote_file="/home/ubuntu/src",
        recurse=True,
    )
    for output in copy_dir_outputs:
        output.get()

    # Copy env file
    copy_env_outputs = client.copy_file(
        local_file=f"{PARENT_DIR}/.env",
        remote_file="/home/ubuntu/.env",
        recurse=True,
    )
    for output in copy_env_outputs:
        output.get()

    # Copy Dockerfile
    copy_docker_outputs = client.copy_file(
        local_file=f"{PARENT_DIR}/docker/backend.dockerfile",
        remote_file="/home/ubuntu/Dockerfile",
        recurse=True,
    )
    for output in copy_docker_outputs:
        output.get()

    # Copy Pipfile
    copy_pipfile_outputs = client.copy_file(
        local_file=f"{PARENT_DIR}/Pipfile",
        remote_file="/home/ubuntu/Pipfile",
        recurse=True,
    )
    for output in copy_pipfile_outputs:
        output.get()

    # Copy Pipfile.lock
    copy_pipfile_outputs_lock = client.copy_file(
        local_file=f"{PARENT_DIR}/Pipfile.lock",
        remote_file="/home/ubuntu/Pipfile.lock",
        recurse=True,
    )
    for output in copy_pipfile_outputs:
        output.get()

    # Build docker
    docker_build_outputs = client.run_command(
        command="docker build . -t service",
    )
    log_outputs(docker_build_outputs)

    # Run docker
    docker_run_outputs = client.run_command(
        command="docker run -d --env-file .env --network host service"
    )
    client.join()
    log_outputs(docker_run_outputs)


if __name__ == '__main__':
    main()
