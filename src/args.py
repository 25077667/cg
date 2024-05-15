"""
This file contains the argument parser for the program.
"""

from argparse import ArgumentParser
import os
from . import __version__


def _get_version() -> str:
    return __version__.__version__


DESCRIPTION = """
A tool to generate commit messages based on the current state of a git repository.
For more details, see: https://github.com/25077667/cg
"""


class Args:
    """
    A singleton to hold the arguments from argparse, so that they can be accessed
    """

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            description=DESCRIPTION,
        )
        self.parser.add_argument(
            "-c",
            "--config",
            type=str,
            default=os.path.join(os.path.expanduser("~"), ".cg", "config.json"),
            help="Path to config file",
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=_get_version(),
        )

        self.args = self.parser.parse_args()

    def __str__(self) -> str:
        return str(self.args)

    def __getitem__(self, key: str):
        return self.args.__getattribute__(key)


args = Args()
