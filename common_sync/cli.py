"""csync cli docstring"""

import click
from click import echo

from common_sync.utils import hello


@click.group()
@click.version_option()
def cli():
    "A simple CLI to search and manage media assets in S3 and locally"


@cli.command()
@click.argument("name")
def hi(name):
    echo(hello(name))
