"""csync cli docstring"""

import click
from click import echo

from common_sync.utils import hello


def echo_dict(input_dict: dict):
    for key, val in input_dict.items():
        echo(f"{key[:18]+'..' if len(key)>17 else key}{(20-int(len(key)))*'.'}{val}")


@click.group()
@click.version_option()
def cli():
    "A simple CLI to search and manage media assets in S3 and locally"


@cli.command()
@cli.argument("name")
def hi(name):
    echo(hello(name))
