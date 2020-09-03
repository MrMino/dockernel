from .main import subparsers


arguments = subparsers.add_parser(
    __name__.split('.')[-1],
    help="Install dockerized kernel into Jupyter"
)
