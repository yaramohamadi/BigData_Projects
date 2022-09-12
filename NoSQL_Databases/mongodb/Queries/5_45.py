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



# Create index
collection.create_index([('hashtags', pymongo.ASCENDING),
                         ('sendTimePersian', pymongo.ASCENDING)],
                        name='tagtime_index')



start = time.time()
a = collection.aggregate([
    # Only keep hashtag and extract date from sendPersianTime
    {"$project": { "_id": 0, "hashtags": 1, "sendDate": {"$substr":['$sendTimePersian',0,10]} }},
    # Only keep days within the input range
    {"$match": {"$and": [{"sendDate": {"$gte": first_day}}, {"sendDate": {"$lte": last_day}}]}},
    # Unwind so each hashtag is a document
    {"$unwind": "$hashtags" },
    # Find number of tweets for each hashtag for each day
    {"$group":{"_id": {"tag": "$hashtags", "Date": "$sendDate"}, "num_of_tweets": {"$sum": 1}}},
    {"$sort": { "num_of_tweets": -1 } },
    # Group by day
    {"$group":{"_id": "$_id.Date", "tag_counts": {"$push": {"tag": "$_id.tag", "num_of_tweets": "$num_of_tweets"}}}},
    {"$sort": { "_id": 1 } },
    # Show only 10 results for each day
    {"$project": {"tag_counts": { "$slice": [ "$tag_counts", 10 ] }}}
    #{"$limit":10}
    ])
for i in a:
    print(i)
print("Time elapsed: ", time.time() - start)





# Remove index
collection.drop_index('tagtime_index')


