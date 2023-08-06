import base64
import git
import requests
from github import Github
from pprint import pprint

def clearCreateRepo(owner,repo,reponame):
    g=Github()
    token="b4fa328e0928e75f6db479645b3cad5e8cd740f3" 
    query_url = f"https://api.github.com/repos/{owner}/{repo}" 
    headers = {
      'Authorization': f'token {token}',
      'Accept': 'application/vnd.github.v3+json',
    }
    r = requests.delete(query_url, headers=headers)
    u=g.get_user()
    repo = u.create_repo(reponame)
    pprint("your repositiory created successfully")