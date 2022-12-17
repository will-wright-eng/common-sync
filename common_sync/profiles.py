"""
Profiles: object-oriented configs that allow for inheritance and helper methods

TODO

there is an aspect of rules that isn't yet captured in these configs
differnt files can be synced in different states and adherence to those rules

states:
- file exists / create if not exists / exact match
- strict = True / False


implement rich: https://rich.readthedocs.io/en/stable/
"""


class Book:
    """
    This base class is intended to include files (pages) that
    occur in all repos. If the file does not exist then a hook
    should be created to populate the repo with cync files
    """

    def __init__(self):
        self.repo_category = "all"
        self.profile_lvl = len(type(self).mro())  # degrees of inheritance
        self.pages = [
            "LICENSE",
            "CODEOWNERS",
            "README.md",
            ".markdownlint.jsonc",
            ".gitignore",
            ".editorconfig",
            ".pre-commit-config.yaml",
        ]
        self.dir_depth = 0  # location of pages from repo root

    def add_cync_file(self):
        "add source-of-truth file to repo"
        pass

    def check_exists(self):
        """
        1. loop through self.pages
        2. check each file exists
        3. add_cync_file if not exists
        """
        pass


class PagePy(Book):
    """
    class docstring
    """

    def __init__(self):
        super().__init__()
        self.repo_category = "python projects"
        self.language = "python"
        self.pages = self.pages + ["Makefile"]


class PagePyApp(Book):
    """
    class docstring
    """

    def __init__(self):
        super().__init__()
        self.repo_category = "python app"
        self.language = "python"
        self.pages = self.pages + [".dockerignore"]


class PageExtension(Book):
    """
    class docstring
    """

    def __init__(self):
        super().__init__()
        self.repo_category = "browser extension"
        self.language = "javascript"
        self.pages = self.pages + [".eslintrc.json"]
        self.dir_depth = 2


class PageReact(Book):
    """
    class docstring
    """

    def __init__(self):
        super().__init__()
        self.repo_category = "react app"
        self.language = "javascript"
