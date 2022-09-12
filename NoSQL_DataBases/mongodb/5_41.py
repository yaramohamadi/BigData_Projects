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
collection.create_index([('senderName', pymongo.ASCENDING)],
                        name='senderName_index')


start = time.time()
a = collection.aggregate([
    {"$group":{"_id": "$senderName", "num_of_tweets": {"$sum": 1}}},
    {"$group":{"_id": {"$cond": 
               { "if": {"$eq": ["$num_of_tweets", 1]}, "then": "1", 
                "else": 
                    {"$cond":
                     { "if": {"$in": ["$num_of_tweets", [2, 3]]}, "then": "2-3",
                      "else": "4-..."}}
                }}, "num_of_users": {"$sum": 1}  }}
    ])
for i in a:
    print(i)
print("Time elapsed: ", time.time() - start)



# Remove index
collection.drop_index('senderName_index')
