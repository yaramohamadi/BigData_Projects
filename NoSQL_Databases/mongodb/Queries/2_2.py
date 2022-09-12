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



# Replace adabic characters with farsi ones
collection.update_many({
    "hashtags": {"$in":[ "فولاد", "شستا", "شبندر" ]}},    
    [{
      "$set" : { "gov": True }
    }]
)
result = collection.find_one({"hashtags": {"$in":[ "فولاد", "شستا", "شبندر" ]}}, {"hashtags": 1, "gov": 1})
print(result)




print("Time elapsed: ", time.time() - start)

