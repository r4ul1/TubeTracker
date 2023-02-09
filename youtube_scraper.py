import requests
import json
from bs4 import BeautifulSoup, Tag


def get_sub_count(name):
    url = f"https://www.youtube.com/results?search_query={name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    scripts: Tag = soup.findAll("script")[33]
    scripts = scripts.get_text().split(" = ", maxsplit=1)[1].rsplit(";", maxsplit=1)[0]
    scripts: dict = json.loads(scripts)
    scripts = scripts["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    for c in range(len(scripts)):
        try:
            subscriber_string = scripts[c]["itemSectionRenderer"]["contents"][0]["channelRenderer"]["videoCountText"]["simpleText"]
            number, unit = subscriber_string.split(" ")
            if '.' in number:
                number = number.replace('.', '')
            if unit == "Mio.":
                number = int(float(number) * 1000000)
            return number
        except Exception as e:
            print(e)