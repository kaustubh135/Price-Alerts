from pymongo import MongoClient


def getDatabase():
    client = MongoClient("mongodb://localhost:27017")
    db = client["price-drop"]
    return db


if __name__ == '__main__':
    getDatabase()
