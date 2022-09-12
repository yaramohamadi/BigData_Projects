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


# # Filter (only search in documents that contain hashtags)
query = { "content": {'$regex': r'#'} }
matches = collection.find(query)

# Create hashtags
for match in matches:
    # Get list of hashtags and insert to corresponding document
    match["hashtags"] = re.findall(r'#(\w+)', match['content'])
    collection.update_one({'id': match['id']}, {"$set": {'hashtags': match["hashtags"]}})
    #print(collection.find_one({"id": match['id']})['hashtags'])
    
    
# Replace adabic characters with farsi ones
collection.update_many(
    { 'content': { "$regex": r'^(?=.*ك)(?=.*ي).*$'}},
    [{
      "$set" : { "content": {
          "$replaceAll": { "input": "$content", "find": "ي", "replacement": "ی"} }}},
     {"$set" : { "content": {
          "$replaceAll": { "input": "$content", "find": "ك", "replacement": "ک"} }}
    }]
)


print("Time elapsed: ", time.time() - start)


print(collection.find_one({})['content'])
print( collection.find_one({})['hashtags'])