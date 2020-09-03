from argparse import ArgumentParser


DESCRIPTION = "Adds docker image to Jupyter as a kernel"

arguments = ArgumentParser(description=DESCRIPTION)
subparsers = arguments.add_subparsers(help='One of the following:',
                                      metavar='subcommand')
