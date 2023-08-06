import base64
import git
import requests
from github import Github
from pprint import pprint

def deleteRepo(owner,repo):
    token="b4fa328e0928e75f6db479645b3cad5e8cd740f3" 
    query_url = f"https://api.github.com/repos/{owner}/{repo}" 
    headers = {
      'Authorization': f'token {token}',
      'Accept': 'application/vnd.github.v3+json',
    }
    r = requests.delete(query_url, headers=headers)