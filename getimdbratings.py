#!/usr/bin/env python3
import requests
import sys
import json
from bs4 import BeautifulSoup
from myproxies import random

def getRatings(url):
    proxy = random()
    ratings = []
    last_page = False
    while not last_page:
        response = requests.get(url, proxies=proxy, headers={'Accept-Language': 'en-US,en;q=0.8'})

        soup = BeautifulSoup(response.content, 'html.parser')
        for rating_row in soup.find_all('div', {'class': 'lister-item-content'}):
            title_element = rating_row.find('a')
            title = title_element.text.strip()
            year = title_element.parent.find('span', {'class': 'lister-item-year'}).text.strip('()')
            rating = int(rating_row.find_all('span', {'class': 'ipl-rating-star__rating'})[1].text)
            ratings.append({'title': title, 'year': year, 'rating': rating})

        next_button = soup.find('a', {'class': 'flat-button lister-page-next next-page'})
        url = 'https://www.imdb.com' + next_button['href'] if next_button is not None else None
        last_page = (next_button is None)

    return ratings

# url format: https://www.imdb.com/user/ur87654321/ratings
imdb_url = sys.argv[1]
print(json.dumps(getRatings(imdb_url), indent=4))
