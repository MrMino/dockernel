import docker
from .main import subparsers, set_subcommand_func
from argparse import Namespace
from pathlib import Path


arguments = subparsers.add_parser(
    __name__.split('.')[-1],
    help="Start a dockernel"
)

# TODO: add a note about how to pull / build an image
# TODO: add a note about default images
arguments.add_argument(
    'image_name',
    help="Name of the docker image to use."
)

# TODO: make this one optional
# TODO: add a help note about it being put into environment variables
# TODO: add a note about how some kernels react when it is not given
arguments.add_argument(
    'connection_file',
    help="The connection file to use."
)


CONTAINER_CONNECTION_SPEC_PATH = '/kernel-connection-spec.json'
CONTAINER_CONNECTION_SPEC_ENV_VAR = 'DOCKERNEL_CONNECTION_FILE'


def start(parsed_args: Namespace) -> int:
    containers = docker.from_env().containers
    image_name = parsed_args.image_name
    connection_file = Path(parsed_args.connection_file)

    # TODO: parametrize connection spec file bind path
    connection_file_mount = docker.types.Mount(
        target=CONTAINER_CONNECTION_SPEC_PATH,
        source=str(connection_file.absolute()),
        type='bind',
        # XXX: some kernels still open connection spec in write mode
        # (I'm looking at you, IPython), even though it's not being written
        # into.
        read_only=False
    )

    env_vars = {
        CONTAINER_CONNECTION_SPEC_ENV_VAR: CONTAINER_CONNECTION_SPEC_PATH
    }

    # TODO: network_mode shouldn't be "host", expose necessary ports only
    # TODO: parametrize possible mounts
    # TODO: log stdout and stderr
    # TODO: use detached=True?
    containers.run(
        image_name,
        auto_remove=True,
        environment=env_vars,
        mounts=[connection_file_mount],
        network_mode='host',
        stdout=True,
        stderr=True
    )

    # TODO: bare numbered exit statusses seem bad
    return 0


set_subcommand_func(parser=arguments, func=start)
