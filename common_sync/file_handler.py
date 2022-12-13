from typing import Any, Dict

import os
import json
import pathlib


class FileHandler:
    """
    class for working with local repos
    """

    def __init__(self):
        self.git_ident = ".git"

    def get_file_list(self):
        return [str(i) for i in pathlib.Path(".").glob("*")]

    def check_git_repo(self, file_path_str):
        return True if ".git" in file_path_str else False

    def check(self, filename):
        """
        check sync against filename in other repos
        """
        if not check_git_repo():
            return False

        if not filename:
            tmp = {}
            for i, file in enumerate(pathlib.Path(".").glob("*")):
                tmp.update({i: file})

            try:
                target_file = tmp[resp]
            except KeyError as e:
                print(e)
        else:
            target_file = filename

        repos = get_repos()
        exists_in = []
        for repo_name, repo_path in repos.items():
            for val in repo_path.glob("*"):
                if str(target_file) == os.path.split(val)[-1]:
                    exists_in.append(repo_name)

        exists_in = list(set(exists_in))

    def get_repos(self, repo_path: str = "repos", level: int = 2) -> Dict[str, Any]:
        root = pathlib.Path.home() / repo_path
        level_str = "/".join(level * ["*"])
        res = {}
        for a in root.glob(level_str):
            if a.is_dir():
                if ".git" in str(a):
                    tmp = str(a).replace(str(root), "").split("/")
                    try:
                        res.update({tmp[tmp.index(".git") - 1]: a.parent})
                    except ValueError as e:
                        pass
        print(f"repos found: {len(res)}")
        return res

    def ls(self, level: int, thing):
        """
        repos: list directories from root with .git directory
        files: list top level files in each repo
        """
        num = 50
        if thing == "repos":
            res = get_repos()
        elif thing == "files":
            res = get_repos(level=1)
            for repo, dot_git_path in res.items():
                for item in dot_git_path.parent.iterdir():
                    item_name = str(item).split("/")[-1]
                    if item.is_dir():
                        pass
                    if item.is_file():
                        pass
