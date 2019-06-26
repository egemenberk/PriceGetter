import requests
from bs4 import element
from bs4 import BeautifulSoup
import json

url = "http://spys.one/en/http-proxy-list/"
test_url = 'https://www.vatanbilgisayar.com/'
proxies = {
    #"http" : "http://159.65.131.90:8118",
    "http" : "http://111.90.188.210:8080"
}
#"https": 'https://95.179.197.111:3128'

def test(test_url, proxy):
    proxies = {proxy[0].lower(): "http://" + proxy[1]}
    try:
        response = requests.get(test_url,proxies=proxies, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        return None
    return response

def get_table(soup):
    table = soup.find_all("tr", {"onmouseover": "this.style.background='#002424'"})
    return table

def get_proxies():
    url = "http://spys.one/en/http-proxy-list/"
    proxies = {}

    for i in range(3):
        page_url = url + str(i) + "/"
        proxy_page = requests.get(page_url)
        soup = BeautifulSoup(proxy_page.text, "html.parser")
        table = get_table(soup)
        for row in table:
            tds = row.find_all("td")
            proxy_url = row.find("font" , {"class":"spy14"}).contents[0]
            proxy_type = "HTTP"
            if "https" in tds[1].find("a")["href"]:
                proxy_type += "S"
            latency = float(tds[5].find("font").text)
            proxies[proxy_url] = (proxy_type, latency)
        #proxy_list = sorted(proxies, key=lambda k: proxies[k][1], reverse=False)
    print("# of proxies fetched: " + str(len(proxies)))
    return proxies

def working_proxies(test_url):
    proxies = get_proxies()
    working_ones = {}
    for url, val in proxies.items():
        if test(test_url, (val[0], url)) != None:
            working_ones[url] = val
    print("# of working_proxies: " + str(len(working_ones)))
    return working_ones

if __name__ == '__main__':
    proxy_list = sorted(proxies, key=lambda k: proxies[k][1], reverse=False)

#print(proxy_url, proxy_type, latency)
