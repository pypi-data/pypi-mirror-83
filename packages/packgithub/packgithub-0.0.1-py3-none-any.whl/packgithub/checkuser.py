import base64
import git
import requests
from github import Github
from pprint import pprint

def checkCredentials(user,password):
  g=Github()
  username = g.get_user(user)
  pprint("Authentication successful!!")
  pprint("Your Repositories are:")
  for repo in username.get_repos():
        pprint(repo.name)