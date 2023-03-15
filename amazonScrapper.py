import requests
from bs4 import BeautifulSoup


def getHeaders():
    return {
        'authority': 'www.amazon.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }


def getSoup(url):
    page = requests.get(url, headers=getHeaders())
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def getPrice(soup):
    fullPrice = soup.select_one("#corePrice_feature_div > div > span > span.a-offscreen")
    # price = soup.select_one("#twister-plus-price-data-price").get("value")
    if fullPrice:
        fullPrice = fullPrice.text
        price = int(fullPrice.split(".")[0][1:].replace(",", ""))
    else:
        fullPrice = "Currently unavailable."
        price = -1
    return price


def getTitle(soup):
    fullTitle = soup.select_one(".product-title-word-break")
    if fullTitle:
        fullTitle = fullTitle.text
    else:
        fullTitle = "Unknown"
    return fullTitle.strip()


