from typing import Mapping

from amazonScrapper import getSoup, getPrice
from datetime import datetime

from pymongo.collection import Collection
from pymongo.database import Database


def updatePrice(productId: str, db: Database, bucketList: Collection, product: Mapping, newPrice: int, prevPrice: int):
    priceHistory = db["priceHistory"]
    priceHistory.insert_one({
        "productId": productId,
        "prevPrice": prevPrice,
        "newPrice": newPrice,
        "createdAt": datetime.today()
    })

    lowPrice = min(product["lowestPrice"], newPrice)
    highPrice = max(product["highestPrice"], newPrice)
    bucketList.update_one({"productId": productId}, {
        "currentPrice": newPrice,
        "lowestPrice": lowPrice,
        "highestPrice": highPrice
    })


def priceCheck(db: Database, productId: str):
    bucketList = db["bucketList"]
    product = bucketList.find_one({"productId": productId})
    target = product["target"]
    soup = getSoup(product["url"])
    newPrice = getPrice(soup)
    prevPrice = product["currentPrice"]
    alertType = product["alertType"]
    if alertType == 0:
        if newPrice <= target:
            updatePrice(productId, db, bucketList, product, newPrice, prevPrice)
            print(f"Price for {product['title']} has changed to {newPrice} from {prevPrice}")
    elif alertType == 1:
        if newPrice <= prevPrice:
            updatePrice(productId, db, bucketList, product, newPrice, prevPrice)
            print(f"Price for {product['title']} has changed to {newPrice} from {prevPrice}")
    elif alertType == 2:
        if newPrice != prevPrice:
            updatePrice(productId, db, bucketList, product, newPrice, prevPrice)
            print(f"Price for {product['title']} has changed to {newPrice} from {prevPrice}")
    else:
        print("Invalid Alert")
