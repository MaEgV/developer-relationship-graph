from pprint import pprint

import requests
import requests.auth as a
import pandas as pd
from src.data_import.reader import get_users_list
from github import Github

def load_users(repo: str, num: int = 50) -> None:
    url = f"https://api.github.com/repos/{repo}/contributors"
    user_data = requests.get(url, params={'per_page': num}).json()
    pd.DataFrame.from_records(user_data).to_csv('../../data/users/users.csv')



def load_commits(repo: str, branches: list, user: str):
    url = f"https://api.github.com/repos/{repo}/commits"
    response_length = 100
    res = list()

    last_sha = 'master'
    counter = 0
    while True:
        print(counter)
        counter += 1
        resp = requests.get(url,
                            params={'author': user,
                                    'per_page': response_length,
                                    'sha': last_sha },
                            headers={'Authorization': 'token -'})
        new_page = resp.json()
        res.extend(new_page)

        if resp.status_code != 200:
            return
        elif len(new_page) < response_length:
            break
        else:
            last_sha = res[-1]['sha']

    pd.DataFrame.from_records(res).to_csv(f'../../data/commits/{user}_commits.csv')


def load_files(input_filename: str, out_filename: str):
    urls = list(pd.read_csv(input_filename)['url'])
    res = list()
    counter = 0
    for url in urls:
        resp = requests.get(url, headers={'Authorization': 'token -'}).json()['files']
        print(counter)
        res.extend(resp)
        counter += 1

    df = pd.DataFrame.from_records(res)
    df = df.drop(['patch'], axis=1)
    df.to_csv(out_filename)


rep = 'facebook/react'
users_path = '../../data/users/'
commits_path = '../../data/commits/'
changes_path = '../../data/changes/'

resp = requests.get(f"https://api.github.com/repos/{rep}/branches",
                    params={
                        'per_page': 100,
                    },
                    headers={'Authorization': 'token -'}).json()

df = pd.DataFrame.from_records(resp)
branches = list(df['name'])


counter = 0
for login in get_users_list(users_path+'users.csv'):
    print(counter, login)
    counter += 1
    load_files(commits_path+login+'_commits.csv', changes_path+login+'_files.csv')
    print('ok')
