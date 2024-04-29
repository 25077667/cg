"""
This file contains the argument parser for the program.
"""

from argparse import ArgumentParser
import os


class Args:
    """
    A singleton to hold the arguments from argparse, so that they can be accessed
    """

    def __init__(self) -> None:
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "-c",
            "--config",
            type=str,
            default=os.path.join(os.path.expanduser("~"), ".cg", "config.json"),
            help="Path to config file",
        )

        self.args = self.parser.parse_args()

    def __str__(self) -> str:
        return str(self.args)

    def __getitem__(self, key: str):
        return self.args.__getattribute__(key)


args = Args()
