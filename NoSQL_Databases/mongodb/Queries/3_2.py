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


a = collection.aggregate([
    # Only keep hashtag (faster)
    {"$project": { "_id": 0, "hashtags": 1 } },
    # Unwind so each hashtag is a document
    {"$unwind": "$hashtags" },
    {"$group":{"_id": "$hashtags", "num_of_tweets": {"$sum": 1}}},
    {"$sort": { "num_of_tweets": -1 } }
    ])

for i in a:
    print(i)



print("Time elapsed: ", time.time() - start)

