import pymongo
from pymongo import MongoClient
import re
import time

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets


first_day = '1400/02/16'
last_day = '1400/02/17'


start = time.time()


a = collection.aggregate([
    # Only keep user and extract date from sendPersianTime
    {"$project": { "_id": 0, "senderName": 1, "sendDate": {"$substr":['$sendTimePersian',0,10]} }},
    # Only keep days within the input range
    {"$match": {"$and": [{"sendDate": {"$gte": first_day}}, {"sendDate": {"$lte": last_day}}]}},
    # Find number of tweets for each user for each day
    {"$group":{"_id": {"name": "$senderName", "Date": "$sendDate"}, "num_of_tweets": {"$sum": 1}}},
    {"$sort": { "num_of_tweets": -1 } },
    # Group by day
    {"$group":{"_id": "$_id.Date", "user_counts": {"$push": {"name": "$_id.name", "num_of_tweets": "$num_of_tweets"}}}},
    {"$sort": { "_id": 1 } },
    # Show only top user for each day
    {"$project": {"user_counts": { "$slice": [ "$user_counts", 1 ] }}}
    ])


for i in a:
    print(i)
    
    
    

print("Time elapsed: ", time.time() - start)

