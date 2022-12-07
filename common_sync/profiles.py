"""docstring"""


class Book:
    def __init__(self):
        self.repo_category = "all"
        self.pages = ["LICENSE", "CODEOWNERS", "README.md", ".markdownlint.jsonc"]


class PagePy(Book):
    def __init__(self):
        super().__init__()
        self.repo_category = "python projects"
        self.profile_lvl = len(type(self).mro())
        self.pages = self.pages.append([".pre-commit-config.yaml"])
