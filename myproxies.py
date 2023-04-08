import requests
from os.path import expanduser
from random import sample

CONFIG_DIR = expanduser('~/.secret')

getServers = lambda: open(f'{CONFIG_DIR}/proxy_list.txt', 'r').read().splitlines()
_username, _password = open(f'{CONFIG_DIR}/proxy_auth.txt', 'r').read().splitlines()

def getProxies():
    serverList = getServers()
    return list(map(lambda server: {
        'https': f'https://{_username}:{_password}@{server}'
    }, sample(serverList, len(serverList))))

random = lambda: getProxies()[0]

def sendRequest(url: str, v=False, **kwargs) -> requests.Response:
    for proxy in getProxies():
        try:
            r = requests.get(url, proxies=proxy, **kwargs)
        except requests.exceptions.ProxyError as e:
            if v:
                print(e)
            pass
        else:
            return r;
    raise requests.exceptions.ProxyError('none of the proxies worked')

__all__ = ["getServers", "getProxies", "random", "sendRequest"]
