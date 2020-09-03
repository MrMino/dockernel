from .main import subparsers


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
