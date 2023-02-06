import requests
import json
from bs4 import BeautifulSoup, Tag


def get_channel_id(name):
    url = f"https://www.youtube.com/results?search_query={name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    scripts: Tag = soup.findAll("script")[33]
    scripts = scripts.get_text().split(" = ", maxsplit=1)[1].rsplit(";", maxsplit=1)[0]
    scripts: dict = json.loads(scripts)
    scripts = scripts["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    for c in range(len(scripts)):
        try:
            print(scripts[c]["itemSectionRenderer"]["contents"][0].keys())
            scripts = scripts[c]["itemSectionRenderer"]["contents"][0]["channelRenderer"]["videoCountText"]["simpleText"]
            print(scripts.split(" ")[0])
            return scripts.split(" ")[0]
        except Exception as e:
            print(e)


def get_subscriber_count(channel_id):
    url = f"https://www.youtube.com/channel/{channel_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    subscriber_count = soup.find("span", {"class=":"meta-item style-scope ytd-c4-tabbed-header-renderer"})
    subscriber_count = soup.select("span[class*='subscriber-count']")
    if subscriber_count:
        return subscriber_count.text
    else:
        subscriber_count = soup.find("span", {"class=":"meta-item style-scope ytd-c4-tabbed-header-renderer"})
    if subscriber_count:
        return subscriber_count.text
    else:
        return "Could not retrieve subscriber count"

def get_channel_subscriber_count(channel_name):
    channel_id = get_channel_id(channel_name)
    if channel_id:
        subscriber_count = get_subscriber_count(channel_id)
        return subscriber_count
    else:
        return "Could not find channel id"
