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



collection.update_many(
        {"parentId": {"$exists": True}},
        { "$unset": { "type": "" } }
)

# We say show type but there is nothing in output so type does not exist anymore
result = collection.find_one({"parentId": {"$exists": True}}, {"parentId": 1, "_id": 0, "type": 1})
print(result)



print("Time elapsed: ", time.time() - start)

