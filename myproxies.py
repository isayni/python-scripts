import os, random

CONFIG_DIR = os.path.expanduser('~/.secret')

def random_proxy():
    servers = open(f'{CONFIG_DIR}/proxy_list.txt', 'r').read().splitlines()
    server = random.choice(servers)
    proxy_username, proxy_password = open(f'{CONFIG_DIR}/proxy_auth.txt', 'r').read().splitlines()
    return {
        'https': f'https://{proxy_username}:{proxy_password}@{server}'
    }
