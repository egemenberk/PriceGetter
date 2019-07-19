import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/itm/CREE-H4-HB2-9003-2000W-300000LM-4-Sides-LED-Headlight-Kit-Hi-Lo-Power-Bulb-6000K/253624141664?_trkparms=pageci%3A035d16a9-aa18-11e9-aa95-74dbd180f92e|parentrq%3A09fb7cf516c0a4e922925f33ffec70de|iid%3A1"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

print(soup.title)
links = soup.find("span", {"itemprop": "name"})
print(links.text.strip())
"""
for cat in links:
    try:
        if "-c-" in cat["href"]:
            print(cat["href"])
    except:
        continue
"""
