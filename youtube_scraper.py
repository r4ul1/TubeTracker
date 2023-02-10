import requests
import json
from bs4 import BeautifulSoup, Tag


# The function retrieves the number of subscribers of a YouTube channel by searching for the channel's name on YouTube's search page.
def get_sub_count(name):
    url = f"https://www.youtube.com/results?search_query={name}&sp=EgIQAg%253D%253D"
# It uses the requests library to make a GET request to the search page and BeautifulSoup to parse the HTML content.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
# The 33rd script tag in the page's source code is found and the relevant information is extracted from the JSON data within the tag.
    scripts: Tag = soup.findAll("script")[33]
    scripts = scripts.get_text().split(" = ", maxsplit=1)[1].rsplit(";", maxsplit=1)[0]
    scripts: dict = json.loads(scripts)
    scripts = scripts["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    for c in range(len(scripts)):
        try:
# The function loops through the contents of the scripts data and tries to extract the subscriber count string in the format of "number unit", such as "111 Mio.".
            subscriber_string = scripts[c]["itemSectionRenderer"]["contents"][0]["channelRenderer"]["videoCountText"]["simpleText"]
# The subscriber count string is then split into two parts: the number and the unit.
            number, unit = subscriber_string.split(" ")
# If there is a dot in the number, the dot is removed. Finally, the function returns the subscriber count as an integer.
            if '.' in number:
                number = number.replace('.', '')
# If the unit is "Mio", the number is converted to an integer by multiplying it by 1000000.
            if unit == "Mio.":
                number = int(float(number) * 1000000)
            return number
        except Exception as e:
            print(e)


def get_most_recent_video_views(name):
    url = f"https://www.youtube.com/results?search_query={name}sp=EgIQAQ%253D%253D"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    scripts: Tag = soup.findAll("script")[33]
    scripts = scripts.get_text().split(" = ", maxsplit=1)[1].rsplit(";", maxsplit=1)[0]
    scripts: dict = json.loads(scripts)
    scripts = scripts["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

    video = scripts[0]["itemSectionRenderer"]["contents"][0]["videoRenderer"]
    title = video["title"]["runs"][0]["text"]
    views = video["viewCountText"]["simpleText"]
    return (title, views)
