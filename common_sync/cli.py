"""csync cli docstring"""

import json
import pathlib
from pprint import pprint

import click
from click import echo

import common_sync.profiles as profiles
from common_sync.utils import hello


@click.group()
@click.version_option()
def cli():
    "A simple CLI to search and manage media assets in S3 and locally"


@cli.command()
@click.argument("name")
def hi(name):
    echo(hello(name))


@cli.command()
def init():
    """
    get relevant project list and store in configs
    """
    echo("TODO")


@cli.command()
@click.option("-f", "--filename", "filename", required=True)
def check(filename):
    """
    check sync against filename in other repos
    """
    echo("TODO")


def formatted_echo(echo_list):
    for ele in echo_list:
        for key, val in ele.items():
            echo(f"{key}{(20-len(key))*'.'}{val}")


def get_repos(for_echo=False, level: int = 2):
    root = pathlib.Path.home() / "repos"
    level_str = "/".join(level * ["*"])

    ident = ".git"
    res = {}
    for a in root.glob(level_str):
        if a.is_dir():
            if ".git" in str(a):
                tmp = str(a).replace(str(root), "").split("/")
                try:
                    res.update({tmp[tmp.index(".git") - 1]: str(a) if for_echo else a})
                except ValueError as e:
                    pass
    return res


@cli.command()
@click.option("-L", "--level", "level", default=2)
@click.argument("thing")
def list(level: int, thing):
    """
    repos: list directories from root with .git directory
    files: list top level files in each repo
    """
    num = 50
    if thing == "repos":
        res = get_repos(for_echo=True)
        echo(json.dumps(res, indent=4))
    elif thing == "files":
        res = get_repos()
        for repo, dot_git_path in res.items():
            echo(f"\n{(4+len(repo))*'#'}")
            echo(f"# {repo.upper()} #")
            echo(f"{(4+len(repo))*'#'}")
            for item in dot_git_path.parent.iterdir():
                item_name = str(item).split("/")[-1]
                if item.is_dir():
                    echo(f"{item_name}{(num-len(item_name))*'.'}dir")
                if item.is_file():
                    echo(f"{item_name}{(num-len(item_name))*'.'}file")
    else:
        echo("invalid arguemnt")
