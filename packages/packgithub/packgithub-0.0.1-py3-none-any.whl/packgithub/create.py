import base64
import git
import requests
from github import Github
from pprint import pprint

def createRepo(reponame):
    g = Github("2e3f647b342094bd5d24839870de1eed15126af2") 
    u=g.get_user()
    repo = u.create_repo(reponame)
    pprint("your repositiory created successfully")
 