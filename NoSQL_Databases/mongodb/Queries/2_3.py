import pymongo
from pymongo import MongoClient
import re
import time

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets


start = time.time()



# Get results for hour = 16 ( Only return 10 results )
results = collection.find({
    "sendTimePersian": {'$regex': r'.*16:'}
    },
    {"senderName": 1, "senderProfileImage": 1, "_id": 0}).limit(10)

for a in results:
    print(a)




print("Time elapsed: ", time.time() - start)

