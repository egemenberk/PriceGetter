import requests
from bs4 import BeautifulSoup


url="https://www.vatanbilgisayar.com/gigabyte-rtx2060-gaming-oc-pro-6gb-gddr6-192bit-nvidia-dx12-ekran-karti.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


