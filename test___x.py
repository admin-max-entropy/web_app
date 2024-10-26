import xml.etree.ElementTree as ET
from ast import parse

import bs4
import feedparser
import requests
import bs4 as bs
from certifi import contents

url = "https://www.federalreserve.gov/feeds/feds_notes.xml"
feed = feedparser.parse(url)
response = requests.get(url)
for entry in feed.entries:
    soup = bs4.BeautifulSoup(entry.summary, features="html.parser")
    text = ""
    for tag in soup.find_all("br"):
        for row in tag.next_siblings:
            text += row.get_text()
        print(text)
        break