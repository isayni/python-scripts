#!/usr/bin/env python
'''
    script to automate downloading movie subtitles from
    https://opensubtitles.org

    unzipping the package, renaming the file and deleting the remains.
'''
import requests
import os
import sys
import zipfile
import json
import time
from bs4 import BeautifulSoup
from termcolor import colored

def printHelp():
    print('''a script to automate downloading movie subtitles from https://opensubtitles.org
unzipping the package, renaming the file and deleting the remains.

Usage:
    opensubtitlesDownloader.py [-l language] [-p] <movie_title> [number]

[number]:      determine which most popular option in turn to download (1 - first, 2 - second etc.)
-l [language]: search for subtitles in given language
-p:            use proxy servers to download
-h, --help:    print this help message''')
    exit()

PATH = os.getcwd()
FILES = os.listdir(PATH)
LANG = 'ENG'
NUMBER = 0 # which most popular option to choose
download = requests.get
CONFIG_DIR = os.path.expanduser('~') + '/.config/opensubtitlesDownloader'

try:
    with open(CONFIG_DIR + '/cookies.txt', 'r') as f:
            COOKIES = json.load(f)
except:
    COOKIES = {}

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '-h' or arg == '--help': # [-h]
        printHelp()
    elif arg == '-l': # [-l language]
        i+=1
        LANG = sys.argv[i].upper()[0:3]
    elif arg == '-p': # [-p]
        from myproxies import sendRequest
        download = sendRequest
        print(colored('using proxies', 'grey'))
    elif arg.isnumeric(): # [number]
        NUMBER = int(arg) - 1
    else: # <movie_title>
        SEARCH = arg
    i+=1

try:
    SEARCH
except:
    printHelp()

# searching the website for the chosen movie
r = requests.get(
    f'https://www.opensubtitles.org/en/search2/sublanguageid-{LANG}/moviename-{SEARCH}'
)
bs = BeautifulSoup(r.text, 'lxml')

# if there is /imdbid- in the url, that means there was only one result
# for our query and we jumped straight to the title page, meaning that we can
# skip this part
if not "/imdbid-" in r.url:
    table = bs.find('table', {'id': 'search_results'})
    row = table.find_all('tr')[1]
    suffix = row.find('a').get('href')
    r = requests.get('https://www.opensubtitles.org/' + suffix)
    bs = BeautifulSoup(r.text, 'lxml')

table = bs.find(id='search_results')
rows = table.find_all('tr')[1:]
TITLE = rows[0].find('a').get_text().split('\n')[0]
print(colored(TITLE, 'yellow'))

allOptions = []

# choosing the right file to download
for row in rows:
    try:
        cell = row.find_all('td')[4]
        a = cell.find('a')
        am = int(a.get_text().split('x')[0])
        if cell.find('span').get_text() == 'srt':
            allOptions.append({'tag': a, 'dws': am})
    except:
        pass

# sorting the list to pick the right one
allOptions = sorted(allOptions, key = lambda i: i['dws'], reverse=True)
chosen = allOptions[NUMBER]

print(f'picking the {str(NUMBER + 1)} most popular option with {str(chosen["dws"])} downloads.')

# downloading
url = 'https://www.opensubtitles.org' + chosen['tag'].get('href')
filename = str(int(time.time())) + '.zip'
open(filename, 'wb').write(download(url, cookies=COOKIES).content)

toRemove = []

# unzipping and removing remaining files
for f in list(set(os.listdir(PATH)) - set(FILES)):
    if f.endswith('.zip'):
        with zipfile.ZipFile(f, 'r') as ref:
            ref.extractall(PATH)
        allFiles = os.listdir(PATH)
        toRemove += list(set(allFiles) - set(FILES))
for f in toRemove:
    if f.endswith('.srt'):
        if LANG == 'POL':
            LANG = 'PL'
        os.rename(f, f'{TITLE}.{LANG.lower()}.srt')
    else:
        os.remove(f)
