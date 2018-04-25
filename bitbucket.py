#!/usr/bin/env python3

import requests
from getpass import getpass
import json
import time

import config


def get_auth(my_login: str, prompt_line: str = "password:"):
    global auth
    if auth is None:
        print('login: {0}'.format(my_login))
        my_pass = getpass(prompt=prompt_line)
        auth = (my_login, my_pass)
    return auth


def reset_auth():
    global auth
    auth = None


def init_session() -> None:
    if auth is not None:
        return
    rest_session.auth = get_auth(my_login=config.my_user_name, prompt_line="bitbucket pass:")
    rest_session.params.update({
    })
    rest_session.verify = config.verify


def pretty_print(json_obj):
    print(str(json.dumps(json_obj, indent=4, separators=(',', ': '))))


rest_session = requests.Session()
auth = None
BB_DEBUG = False
NETWORK_ERROR_WAIT_DELAY = 10  # ten seconds


def get_prs_url(project: str, repo: str) -> str:
    return config.bb_url + '/rest/api/1.0/projects/' + project + '/repos/' + repo + '/pull-requests'


def download_prs(project: str, repo: str):
    return download(get_prs_url(project, repo))


def get_pr_url(project: str, repo: str, pr_id: int) -> str:
    return '{0}/rest/api/1.0/projects/{1}/repos/{2}/pull-requests/{3}' \
            .format(config.bb_url, project, repo, pr_id)


def download_pr(project: str, repo: str, pr_id: int):
    return download(get_pr_url(project, repo, pr_id))


def get_pr_all_url(project: str, repo: str, pr_id: int) -> str:
    return get_pr_url(project, repo, pr_id) + '/activities'


def download_pr_all(project: str, repo: str, pr_id: int) -> str:
    return download(get_pr_all_url(project, repo, pr_id))


def download(url: str):
    result = None
    while True:
        try:
            init_session()
            r = rest_session.get(url)
            if r.status_code != 200:
                print(r)
                print("Download failed for repo ", repo)
                if r.status_code == 401:
                    print("Wrong password")
                    reset_auth()
                    # go into while True again, ask for password one more time
                    continue
                if r.status_code == 403:
                    print("Need to enter CAPTCHA in the web Bitbucket interface")
                    reset_auth()
                    continue
                if r.status_code == 404:
                    print("No repository ", repo)
                break
            else:
                if BB_DEBUG:
                    print("url: ", url)
                    print("Request successful")
                result = r.json()
                break
        except requests.exceptions.ConnectionError as ce:
            print("Connection error: ", ce)
            print("You might need to define 'verify' in config.py.")
            print("Current value: config.verify =", config.verify)
            print("Waiting for {0} seconds...".format(NETWORK_ERROR_WAIT_DELAY))
            time.sleep(NETWORK_ERROR_WAIT_DELAY)
            # might be useless to try again, return None
            break
    return result
