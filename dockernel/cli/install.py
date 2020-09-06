import platform
import docker
from typing import List
from argparse import Namespace
from .main import subparsers, set_subcommand_func
from ..kernelspec import (Kernelspec, user_kernelspec_store,
                          ensure_kernelspec_store_exists, kernelspec_dir,
                          install_kernelspec)


arguments = subparsers.add_parser(
    __name__.split('.')[-1],
    help="Install dockerized kernel image into Jupyter."
)
arguments.add_argument(
    'image_name',
    help="Name of the docker image to use."
)
arguments.add_argument(
    '--name',
    help="Display name for the kernelspec. "
    "By default, container hostname is used.",
    default=None
)
arguments.add_argument(
    '--language', '-l',
    help="Language used by the kernel. "
    "Makes notebooks written in a given language "
    "run on different kernels, that use the same language, "
    "if this one is not found. "
    "By default, empty value is used.",
    default=''
)


JUPYTER_CONNECTION_FILE_TEMPLATE = '{connection_file}'


def generate_kernelspec_argv(image_name: str) -> List[str]:
    python_cmd = ['/usr/bin/env', 'python', '-m']
    dockernel_cmd = ['dockernel', 'start',
                     image_name, JUPYTER_CONNECTION_FILE_TEMPLATE]
    return python_cmd + dockernel_cmd


def image_digest(docker_client: docker.client.DockerClient,
                 image_name: str) -> str:
    image = docker_client.images.get(image_name)
    return image.attrs['ContainerConfig']['Hostname']


def install(args: Namespace) -> int:
    system_type = platform.system()
    store_path = user_kernelspec_store(system_type)
    ensure_kernelspec_store_exists(store_path)

    argv = generate_kernelspec_argv(args.image_name)
    display_name = args.image_name if args.name is None else args.name
    language = args.language

    kernelspec = Kernelspec(argv, display_name, language)

    docker_client = docker.from_env()
    kernel_id = image_digest(docker_client, args.image_name)
    location = kernelspec_dir(store_path, kernel_id)
    install_kernelspec(location, kernelspec)

    # TODO: bare numbered exit statusses seem bad
    return 0


set_subcommand_func(parser=arguments, func=install)
