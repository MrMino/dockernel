from typing import List
from .cli import main_arguments


def run(argv: List) -> int:
    main_arguments.parse_args(argv[1:])
    return 0
