from mongoConnection import getDatabase
from utils import displayDetails

if __name__ == '__main__':
    db = getDatabase()
    bucketList = db["bucketList"]
    displayDetails(bucketList)
    x = int(input())
    match x:
        case 0: # List all add Products
            displayDetails(bucketList)
        case 1:
            pass
