import re
from typing import List

from pymongo.collection import Collection
from amazonScrapper import getSoup, getPrice, getHeaders, getTitle


def parseUrl(url: str) -> tuple[str, str]:
    parsedUrl = re.findall(r"(https?://www.amazon.in/.*/(?:dp|gp)/(.*)/?).*", url)
    if parsedUrl:
        if len(parsedUrl[0]) == 2:
            return parsedUrl[0][0], parsedUrl[0][1]
        else:
            raise f"No id found for {url}"
    else:
        raise f"Invalid Url {url}"


def getUrls(col: Collection) -> List:
    urls = []
    for i in col.find():
        urls.append(i)
    return urls


def addUrl(col: Collection, url: str, alertType: int, target: int = None):
    parsedUrl = parseUrl(url)
    if not col.find_one({"productId": parsedUrl[1]}):
        soup = getSoup(parsedUrl[0])
        price = getPrice(soup)
        title = getTitle(soup)
        col.insert_one({
            "url": parsedUrl[0],
            "productId": parsedUrl[1],
            "target": target,
            "title": title,
            "alertType": alertType,
            "currentPrice": price,
            "lowestPrice": price,
            "highestPrice": price
        })
    else:
        print("Already available")


def addManyUrls(col: Collection, urls: List):
    for url in urls:
        addUrl(col, url["url"], url["alertType"], url["target"])


def removeUrl(col: Collection, productId: str):
    col.delete_one({"productId": productId})


if __name__ == '__main__':
    from mongoConnection import getDatabase

    priceAlert = getDatabase()["bucketList"]
    # addUrl(priceAlert,"https://www.amazon.in/Razer-Gaming-Programmable-Buttons-Optical/dp/B084W6W9WB/ref=sr_1_1?crid=76KZYBZXKZE3&keywords=razer%2Bviper&qid=1670510147&sprefix=razor%2Bvipe%2Caps%2C243&sr=8-1&th=1",0, 1000)
    addManyUrls(priceAlert, [{'url':'https://www.amazon.in/Redgear-Gaming-Semi-Honeycomb-Windows-Gamers/dp/B08CHZ3ZQ7','productId':'B08CHZ3ZQ7','target':200,'alertType':0},{'url':'https://www.amazon.in/Redgear-Gaming-Mouse-Upto-4800/dp/B07N6LN57W','productId':'B07N6LN57W','target':400,'alertType':0},{'url':'https://www.amazon.in/Logitech-G102-Customizable-Lighting-Programmable/dp/B08LT9BMPP','productId':'B08LT9BMPP','target':1000,'alertType':0},{'url':'https://www.amazon.in/Lenovo-Legion-Gaming-Ergonomic-ambidextrous/dp/B08D4KH7RN','productId':'B08D4KH7RN','target':1000,'alertType':0},{'url':'https://www.amazon.in/Redgear-X12-Customization-programmable-Buttons/dp/B09FLD6BJN','productId':'B09FLD6BJN','target':1000,'alertType':0},{'url':'https://www.amazon.in/Razer-DeathAdder-RZ01-02540100-R3M1-Essential-Optical/dp/B07F2GC4S9','productId':'B07F2GC4S9','target':1000,'alertType':0},{'url':'https://www.amazon.in/Razer-Gaming-Programmable-Buttons-Optical/dp/B084W6W9WB','productId':'B084W6W9WB','target':1000,'alertType':0},{'url':'https://www.amazon.in/Seagate-Expansion-2TB-External-HDD/dp/B08ZJG6TVT','productId':'B08ZJG6TVT','target':5000,'alertType':0},{'url':'https://www.amazon.in/Seagate-Touch-External-Password-Protection/dp/B094QZLJQ6','productId':'B094QZLJQ6','target':5000,'alertType':0},{'url':'https://www.amazon.in/Elements-Portable-External-Drive-Black/dp/B00PLOXG42','productId':'B00PLOXG42','target':5000,'alertType':0},{'url':'https://www.amazon.in/Passport-Portable-External-Drive-Black/dp/B07VTFN6HM','productId':'B07VTFN6HM','target':5000,'alertType':0}])
    print(getUrls(priceAlert))
