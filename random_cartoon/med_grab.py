import os
import random
import string

import requests
from bs4 import BeautifulSoup

# The Cartoons are found on this website
URL = 'https://www.b98.tv/'

# Create Headers neatly (taken from HTTP Request in dev tools)
# We need a user agent otherwise the page returns a 403
UAA = 'Mozilla/5.0'
OS = '(Macintosh; Intel Mac OS X 10_13_6)'
ENGINE = 'AppleWebKit/537.36 (KHTML, like Gecko)'
CLIENT = 'Chrome/81.0.4044.113 Safari/537.36'
HEADERS = {'User-Agent':  f'{UAA} {OS} {ENGINE} {CLIENT}'}


def get_page(url):
    '''returns a parsed html page'''
    result = requests.get(url, headers=HEADERS).text
    return BeautifulSoup(result, 'html.parser')


def clean_title(title):
    '''returns a string with punctuation removed
    and hypens instead of spaces'''
    title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ', '-')
    return title


def get_item_url(url):
    '''On the cartoon website all lists contain
    *items*. This returns the url to a random item'''
    page = get_page(url)
    items = page.find_all(class_='item')
    return random.choice(items).a['href']


def get_video_url(episode_url):
    '''guess the name of a specific video by grabbing its title,
    cleaning it and then appending .mp4'''
    video_page = get_page(episode_url)
    title = video_page.find(class_='post-title').text
    cleaned_title = clean_title(title)
    return f"https://www.b98.tv/video/{cleaned_title}.mp4"


def is_valid_url(url):
    result = requests.head(url, headers=HEADERS, allow_redirects=False)
    return result.status_code == 200


def main():
    cartoon_url = get_item_url(URL)
    episode_url = get_item_url(cartoon_url)
    video_url = get_video_url(episode_url)

    if is_valid_url(video_url):
        os.system(f"python3 cocoavlc.py '{video_url}'")
    else:
        print(f'Cartoon URL: {cartoon_url}')
        print(f'Episode URL: {episode_url}')
        print(f'Video URL: {video_url}')
        print("URL not valid, trying again.")
        main()


if __name__ == "__main__":
    main()
