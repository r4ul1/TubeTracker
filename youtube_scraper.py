import requests
from bs4 import BeautifulSoup

def get_channel_id(name):
    url = f"https://www.youtube.com/results?search_query={name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    channel_link = soup.find("a", {"class": "yt-uix-tile-link"})
    if channel_link:
        return channel_link["href"].split("/")[-1]
    else:
        return None

def get_subscriber_count(channel_id):
    url = f"https://www.youtube.com/channel/{channel_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    subscriber_count = soup.find("subscriber-count", {"class=":"meta-item style-scope ytd-c4-tabbed-header-renderer"})
    subscriber_count = soup.select("span[class*='subscriber-count']")
    if subscriber_count:
        return subscriber_count.text
    else:
        subscriber_count = soup.find("subscriber-count", {"class=":"meta-item style-scope ytd-c4-tabbed-header-renderer"})
        if subscriber_count:
            return subscriber_count.text
        else:
            return "Could not retrieve subscriber count"
