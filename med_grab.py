import os
import random
import ssl

import requests
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

# The Cartoons are found on this website
URL = 'https://www.b98.tv/'

# Create Headers Neatly (taken from HTTP Request in dev tools)
# We need a user agent otherwise the page returns a 403
UAA = 'Mozilla/5.0'
OS = '(Macintosh; Intel Mac OS X 10_13_6)'
ENGINE = 'AppleWebKit/537.36 (KHTML, like Gecko)'
CLIENT = 'Chrome/81.0.4044.113 Safari/537.36'
USER_AGENT = f'{UAA} {OS} {ENGINE} {CLIENT}'
HEADERS = {'User-Agent':  USER_AGENT}

def get_page(url):
    '''returns a parsed html page'''
    result = requests.get(url, headers=HEADERS).text
    return BeautifulSoup(result, 'html.parser')


def get_cartoon_url(url):
    '''returns a list of cartoon series'''
    cartoons_page = get_page(url)
    cartoons = cartoons_page.find_all(class_='item')
    return random.choice(cartoons).a['href']


def get_episode_url(episodes_url):
    episodes_page = get_page(episodes_url)
    episodes = episodes_page.find_all(class_='item')
    return random.choice(episodes).a['href']


def get_video_url(episode_url):
    video_page = get_page(episode_url)
    title = video_page.find(class_='post-title')
    stripped_title = title.text.strip()

    # We are essentially just guessing what the
    # title is, generally that means removing punctuation,
    # and replacing spaces with hyphens
    if stripped_title[0] == '-':
        stripped_title.remove('-')
    stripped_title = stripped_title.replace(' ', '-')
    stripped_title = stripped_title.replace("’", '')
    stripped_title = stripped_title.replace("'", '')
    stripped_title = stripped_title.replace(',', '')
    stripped_title = stripped_title.replace('!', '')
    stripped_title = stripped_title.replace('?', '')

    return f"https://www.b98.tv/video/{stripped_title}.mp4"


# Main Loop
searching = True
while searching:
    cartoon_url = get_cartoon_url(URL)
    episode_url = get_episode_url(cartoon_url)
    video_url = get_video_url(episode_url)

    # For Debugging Purposes
    print(f'Cartoon URL: {cartoon_url}')
    print(f'Episode URL: {episode_url}')
    print(f'Video URL: {video_url}')

    # We need to test if the video exists, we do this by getting
    # the head of the HTTP request.
    result = requests.head(video_url, headers=HEADERS, allow_redirects=False)
    if result.status_code == 200:
        print('Web site exists')
        # This might fail if the video's title doesn't match
        # the file's title.
        os.system(f"python cocoavlc.py '{video_url}'")
        searching = False
    else:
        print('Web site does not exist')
