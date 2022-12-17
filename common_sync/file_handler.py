from typing import Any, Dict

import os
import difflib
import pathlib
from pprint import pprint


class FileHandler:
    """class for working with local repos"""

    def __init__(self):
        self.repo_ident = ".git"
        self.repo_path = "repos"
        self.target_file = None
        self.target_file_pattern = None
        self.target_repos = None
        self.sot_file_name = None
        self.sot_file_contents = None

    # set
    def set_target_file_pattern(self, file_name_str):
        self.target_file_pattern = file_name_str

    def set_repo_path(self, repo_path):
        self.repo_path = repo_path

    def set_sot_file_name(self, file_name):
        self.sot_file_name = file_name

    def set_sot_file_contents(self, file_name):
        self.sot_file_contents = file_contents

    def set_target_file(self, file_name):
        # check configs for corresponding sot file
        resp = self.check_for_sot()
        if resp:
            # get sot file contents
            self.sot_file_contents = None  # TODO
        else:
            self.target_file = file_name

    # get
    def get_file_list_str(self):
        return [str(i) for i in pathlib.Path(".").glob("*")]

    def get_file_list_path(self):
        return [i for i in pathlib.Path(".").glob("*")]

    def get_file_list_path_at_level(self, level: int = 2):
        level_str = "/".join(level * ["*"])
        return [i for i in pathlib.Path(".").glob(level_str)]

    def get_files_in_dir(self):
        return [f for f in pathlib.Path(".").glob("**/*") if f.is_file()]

    def get_files_in_wd(self):
        return [f for f in pathlib.Path(".").iterdir() if f.is_file()]

    def get_dir_path(self):
        self.get_file_list_path()

    def get_file_contents(self, file_path):
        with open(file_path) as file:
            tmp = file.read()
        return tmp

    def get_repo_target_path_list(self):
        res = []
        repos_list = self.get_repos_bylevel()
        for key, val in repos_list.items():
            for file in val.iterdir():
                if file.is_file() and self.target_file in str(file):
                    res.append(file)
        return res

    def get_repos_bylevel(self, level: int = 3) -> Dict[str, Any]:
        """
        1. get assets down levels from repos path
        2. check only for directories
        """
        root = pathlib.Path.home() / self.repo_path
        level_str = "/".join(level * ["*"])
        res = {}
        for a in root.glob(level_str):
            if a.is_dir():
                # if self.repo_ident in str(a):
                if ".git" in str(a) and ".github" not in str(a):
                    tmp = str(a.relative_to(root)).split("/")[0]
                    # tmp = str(a).replace(str(root), "").split("/")
                    try:
                        # res.update({tmp[tmp.index(self.repo_ident) - 1]: a.parent})
                        res.update({tmp: root / tmp})
                    except ValueError as e:
                        pass

        if len(res) == 0:
            print("no repos found at this level")
            return False
        else:
            print(f"repos found: {len(res)}")
            return res

    def get_targets(self):
        all_file_paths = self.get_files_in_dir()
        target_file_paths = [file_path for file_path in all_file_paths if self.target_file_pattern in str(file_path)]
        res = {}
        for target in target_file_paths:
            print(str(target))
            tmp = self.get_file_contents(target)
            res[str(target)] = {"file_path": target, "file_contents": tmp}
        return res

    # check
    def check_for_sot(self):
        # TODO
        return False

    def check_wd_for_git_repo(self):
        return True if self.repo_ident in self.get_file_list_str() else False

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

        repos = self.get_repos_bylevel()
        exists_in = []
        path_list = []
        for repo_name, repo_path in repos.items():
            for val in repo_path.glob("*"):
                if str(self.target_file) == os.path.split(val)[-1]:
                    exists_in.append(repo_name)

        pprint(list(set(exists_in)))
        self.target_repos = exists_in

    # compare
    def compare_targets_wd(self):
        """
        compare target files in working directory
        """
        res = self.get_targets()
        if self.sot_file_name:
            # get sot file contents
            # sot_dict = {'file_path': target, 'file_contents':tmp}
            pass
        else:
            # set first file as sot
            sot_file_name = next(iter(res))
            sot_dict = res.pop(sot_file_name)

        for file in list(res):
            # test against sot
            f1_text, f2_text = res.get(file).get("file_contents").split("\n"), sot_dict.get("file_contents").split("\n")
            f1_name, f2_name = file, sot_file_name
            for line in difflib.unified_diff(f1_text, f2_text, fromfile=f1_name, tofile=f2_name):
                print(line)
        return res

    def compare_targets_sot(self):
        """
        compare target file in repos against source of truth
        """
        # TODO
        pass

    # other
    def handle_resp(self, resp):
        if isinstance(resp, int):
            return resp
        else:
            return self.handle_resp(int(resp))

    def ls(self, level: int, thing):
        """
        repos: list directories from root with .git directory
        files: list top level files in each repo
        """
        if thing == "repos":
            res = self.get_repos_bylevel()
        elif thing == "files":
            res = self.get_repos(level=1)
            for repo, dot_git_path in res.items():
                for item in dot_git_path.parent.iterdir():
                    # item_name = str(item).split("/")[-1]
                    if item.is_dir():
                        pass
                    if item.is_file():
                        pass
