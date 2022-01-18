#!/usr/bin/env python
'''
    script to automate downloading movie subtitles from
    https://opensubtitles.org

    unzipping the package, renaming the file and deleting the remains.
'''
import requests
import os
import sys
import wget
import zipfile
from bs4 import BeautifulSoup

PATH = os.getcwd()
FILES = os.listdir(PATH)
# which most popular option to choose
NUMBER = 0

for i in range(1, len(sys.argv)):
    if sys.argv[i].isnumeric():
        NUMBER = int(sys.argv[i]) - 1
    else:
        SEARCH = sys.argv[i]

try:
    SEARCH
except:
    SEARCH = input()

# searching the website for the chosen movie
r = requests.get('https://www.opensubtitles.org/en/search2/sublanguageid-eng/moviename-' + SEARCH)
bs = BeautifulSoup(r.text, "lxml")
table = bs.find("table", {"id": "search_results"})
row = table.find_all("tr")[1]
TITLE = row.find("a").get_text().split("\n")[0]
suffix = row.find("a").get("href")

print(TITLE)

r = requests.get('https://www.opensubtitles.org/' + suffix)
bs = BeautifulSoup(r.text, 'lxml')
table = bs.find(id="search_results")
rows = table.find_all("tr")[1:]

allOptions = []

# choosing the right file to download
for row in rows:
    try:
        cell = row.find_all('td')[4]
        a = cell.find('a')
        am = int(a.get_text().split('x')[0])
        if cell.find('span').get_text() == 'srt':
            allOptions.append({"tag": a, "dws": am})
    except:
        pass

# sorting the list to pick the right one
allOptions = sorted(allOptions, key = lambda i: i['dws'], reverse=True)
chosen = allOptions[NUMBER]

print("picking the " + str(NUMBER + 1) + " most popular option with " + str(chosen["dws"]) + " downloads.")

# downloading
url = "https://www.opensubtitles.org" + chosen["tag"].get('href')
wget.download(url)
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
        os.rename(f, TITLE + " - ENG.srt")
    else:
        os.remove(f)