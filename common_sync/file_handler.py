from typing import Any, Dict

import os
import pathlib


class FileHandler:
    """class for working with local repos"""

    def __init__(self):
        self.repo_ident = ".git"
        self.repo_path = "repos"

    # set
    def set_target_file(self, file_name):
        self.target_file = file_name

    def set_repo_path(self, repo_path):
        self.repo_path = repo_path

    # get
    def get_file_list_str(self):
        return [str(i) for i in pathlib.Path(".").glob("*")]

    def get_file_list_path(self):
        return [i for i in pathlib.Path(".").glob("*")]

    def get_repos(self, level: int = 2) -> Dict[str, Any]:
        root = pathlib.Path.home() / self.repo_path
        level_str = "/".join(level * ["*"])
        res = {}
        for a in root.glob(level_str):
            if a.is_dir():
                if self.repo_ident in str(a):
                    tmp = str(a).replace(str(root), "").split("/")
                    try:
                        res.update({tmp[tmp.index(self.repo_ident) - 1]: a.parent})
                    except ValueError as e:
                        pass
        print(f"repos found: {len(res)}")
        return res

    def check_wd_for_git_repo(self):
        return True if self.repo_ident in self.get_file_list_str() else False

    def handle_resp(self, resp):
        if isinstance(resp, int):
            return resp
        else:
            return self.handle_resp(int(resp))

    # methods
    def check_repos(self, file_name=None):
        """
        check sync against file_name in other repos
        """
        if not self.check_wd_for_git_repo():
            return False

        if not file_name:
            tmp = {}
            for i, file in enumerate(self.get_file_list_path()):
                tmp.update({i: file})
                print(f"{str(i)} {(5-len(str(i)))*'-'} {file}")

            resp = self.handle_resp(input("Which file? [int]"))
            try:
                self.target_file = tmp[resp]
            except KeyError as e:
                print(e)
        else:
            self.target_file = file_name

        repos = self.get_repos()
        exists_in = []
        for repo_name, repo_path in repos.items():
            for val in repo_path.glob("*"):
                if str(self.target_file) == os.path.split(val)[-1]:
                    exists_in.append(repo_name)

        exists_in = list(set(exists_in))

    def ls(self, level: int, thing):
        """
        repos: list directories from root with .git directory
        files: list top level files in each repo
        """
        if thing == "repos":
            res = self.get_repos()
        elif thing == "files":
            res = self.get_repos(level=1)
            for repo, dot_git_path in res.items():
                for item in dot_git_path.parent.iterdir():
                    # item_name = str(item).split("/")[-1]
                    if item.is_dir():
                        pass
                    if item.is_file():
                        pass
