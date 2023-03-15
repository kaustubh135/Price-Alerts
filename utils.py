from pymongo.collection import Collection
from tabulate import tabulate


def displayDetails(col: Collection):
    data = [("Product ID", "Name", "Current Price", "Lowest Price", "Highest Price", "Alert Type")]
    for product in col.find():
        data.append((product["productId"], product["title"][:50], product["currentPrice"], product["lowestPrice"],
                     product["highestPrice"], product["alertType"]))
    print(tabulate(data, headers="firstrow"))
