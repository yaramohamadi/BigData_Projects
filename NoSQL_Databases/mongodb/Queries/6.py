import pymongo
from pymongo import MongoClient
import re
import time

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets

# Create retweets collection
retweets = db["retweets"]

# find retweets from old collection and copy to new collection
collection.aggregate([{ "$match": {"type": "retwit"} }, { "$out": "retweets" }])
a = retweets.find_one({}, {"type": 1})
print(a)

# remove from old collection
collection.delete_many({"type": "retwit"})
