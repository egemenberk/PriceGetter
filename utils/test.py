import requests
from bs4 import BeautifulSoup

url = "https://www.newegg.com/amd-ryzen-5-3600x/p/N82E16819113568?Description=ryzen&cm_re=ryzen-_-19-113-568-_-Product"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

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
