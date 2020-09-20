from typing import Callable
from argparse import ArgumentParser, Namespace


DESCRIPTION = "Adds docker image to Jupyter as a kernel"

arguments = ArgumentParser(description=DESCRIPTION)
# TODO: add required=True when 3.6 compat is dropped
subparsers = arguments.add_subparsers(help='One of the following:',
                                      metavar='subcommand')


def set_subcommand_func(parser: ArgumentParser,
                        func: Callable[[Namespace], int]) -> None:
    parser.set_defaults(func=func)


def run_subcommand(parsed_args: Namespace) -> int:
    # TODO: after 3.6 compat is dropped, the if block below becomes redundant
    if 'func' not in parsed_args:
        arguments.print_help()
        return 1
    return parsed_args.func(parsed_args)
