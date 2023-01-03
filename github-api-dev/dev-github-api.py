# %reset -f

import os
import base64
import datetime as dt
from pprint import pprint
from os.path import join, dirname

import pandas as pd
import requests
from dotenv import load_dotenv
from github import Github

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GH_TOKEN = os.environ.get("GH_TOKEN")

g = Github(GH_TOKEN)

username = "will-wright-eng"
user = g.get_user(username)

# file_str = file.decoded_content.decode()


def get_repo_info(repo):
    print(repo.name)
    return {
        "repo_name": repo.name,
        "repo_full_name": repo.full_name,
        "description": repo.description,
        "date_created": repo.created_at,
        "date_last_modified": repo.pushed_at,
        "home_page": repo.homepage,
        "language": repo.language,
        "num_forks": repo.forks,
        "num_stars": repo.stargazers_count,
        "content_tree": get_repo_tree(repo),
    }


def extract_content_tree(file_or_dir):
    if file_or_dir.type == "file":
        return {"file_name": file_or_dir.name}
    elif file_or_dir.type == "dir":
        content_list = requests.get(file_or_dir.raw_data.get("url")).json()
        return content_list


def get_repo_tree(repo):
    content_list = repo.get_contents("")
    res = {}
    for file_or_dir in content_list:
        res.update({file_or_dir.name: extract_content_tree(file_or_dir)})
    return res


def days_between(d1, d2):
    d1 = dt.datetime.strptime(d1, "%Y-%m-%d")
    d2 = dt.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def main():
    tmp = [get_repo_info(repo) for repo in user.get_repos()]
    df = pd.DataFrame(tmp)
    df["date_last_modified_str"] = df.date_last_modified.astype(str)
    df["date_days_old"] = df.apply(
        lambda x: days_between(x["date_last_modified_str"].split(" ")[0], str(dt.datetime.today()).split(" ")[0]),
        axis=1,
    )
    pprint(df.loc[df.date_days_old < 90])


if __name__ == "__main__":
    main()
