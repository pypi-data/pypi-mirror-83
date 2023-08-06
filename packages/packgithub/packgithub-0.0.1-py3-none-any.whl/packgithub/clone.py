import base64
import git
import requests


def cloneRepo(url,path):
    git.Repo.clone_from(url,to_path=path)