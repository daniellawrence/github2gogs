#!/usr/bin/env python
import requests
import getpass
import json


gitlab_base_url = 'https://git.dansysadm.com/api/v1'
github_repo_url = 'https://api.github.com/users/{username}/repos?per_page=1000'
gitlab_migrate_url = '{0}/repos/migrate'.format(gitlab_base_url)
gitlab_user_url = '{0}/users/{{username}}'.format(gitlab_base_url)


def find_all_github_repos(username):
    url = github_repo_url.format(**locals())
    repo_list = requests.get(url).json()
    return repo_list


def migrate_to_gogs(username, password=None):

    gitlab_user_dict = requests.get(gitlab_user_url.format(**locals())).json()
    if not password:
        password = getpass.getpass("Password for {username}@gogs: ".format(**locals()))

    repo_list = find_all_github_repos(username)

    for github_repo in repo_list:
        print("Migrating {}".format(github_repo.get('name')))
        new_repo_dict = {
            "clone_addr": github_repo.get('html_url'),
            "uid": gitlab_user_dict.get('id'),
            "repo_name": github_repo.get('name'),
            "description": github_repo.get('description'),
        }
        r = requests.post(
            gitlab_migrate_url,
            auth=(username, password),
            data=new_repo_dict)
        print("{:<10} {.text}".format(r))


if __name__ == '__main__':
    migrate_to_gogs('daniellawrence')
