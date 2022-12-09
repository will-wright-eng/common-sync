"""csync cli docstring"""

import os
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


def check_git_repo():
    tmp = [str(i) for i in pathlib.Path(".").glob("*")]
    if ".git" in tmp:
        echo("lacation: in git repo root")
        # echo_list(tmp)
        return True
    else:
        echo(".git not found; move to root of git repo", err=True)
        echo_list(tmp)
        return False


@cli.command()
@click.option("-f", "--filename", "filename", default=None)
def check(filename):
    """
    check sync against filename in other repos
    """
    if not check_git_repo():
        return False

    if not filename:
        tmp = {}
        for i, file in enumerate(pathlib.Path(".").glob("*")):
            echo(f"{str(i)} {(5-len(str(i)))*'-'} {file}")
            tmp.update({i: file})

        resp = click.prompt("Which file?", type=int)
        try:
            target_file = tmp[resp]
            echo(f"checking {target_file}")
        except KeyError as e:
            echo(e)
            echo("invalid value provided")
    else:
        target_file = filename

    repos = get_repos(for_echo=False)
    exists_in = []
    # check repos for target file
    # echo(repos)
    for repo_name, repo_path in repos.items():
        print(repo_path)
        for val in repo_path.glob("*"):
            # print(f"{target_file} -- {str(target_file) == os.path.split(val)[-1]} --{os.path.split(val)[-1]}")
            # exists_in.append(set([i for i in repo_path.glob('*') if target_file==i])[0])
            if str(target_file) == os.path.split(val)[-1]:
                exists_in.append(repo_name)

    exists_in = list(set(exists_in))
    echo(f"matching repos: {len(exists_in)}")
    echo_list(exists_in)


def echo_list(list_obj):
    for obj in list_obj:
        echo("\n")
        echo(f"- {str(obj)}")


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
                    res.update({tmp[tmp.index(".git") - 1]: str(a) if for_echo else a.parent})
                except ValueError as e:
                    pass
    echo(f"repos found: {len(res)}")
    return res


@cli.command()
@click.option("-L", "--level", "level", default=2)
@click.argument("thing")
def ls(level: int, thing):
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
