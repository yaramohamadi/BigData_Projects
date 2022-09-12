import pymongo
from pymongo import MongoClient
import re
import time

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets


# Create index
collection.create_index([('mediaContentType', pymongo.ASCENDING),
                         ('parentID', pymongo.ASCENDING)],
                        name='media_parent_index')


# Nothing is changed here
start = time.time()

results = collection.find({
    "$and":[
        {"mediaContentType" : "image/jpeg"},
        {"parentId": {"$exists": True}}
        ]},
    {"senderName": 1, "_id": 0})

for a in results:
    print(a)
    
print("Time elapsed: ", time.time() - start)
    

# Remove index
collection.drop_index('media_parent_index')