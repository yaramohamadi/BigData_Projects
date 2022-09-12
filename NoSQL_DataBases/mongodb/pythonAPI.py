import requests, json
import pymongo
from pymongo import MongoClient
import re
from time import sleep

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets

url = 'https://www.sahamyab.com/guest/twiter/list?v=0.1'
seenIds = set()
total = 1000

while collection.estimated_document_count() < total: 
    # Get 10 tweets
    response = requests.get(url, headers={'User-Agent': 'Chrome/61'})
    if response.status_code != 200:
        print('HTTP', response.status_code)
        continue

    data = response.json()["items"]
    for tweet in data:
        # Save to mongo if we not seen this tweet
        if tweet["id"] not in seenIds:
            try:
                #tweet["hashtags"] = re.findall(r'#(\w+)', tweet['content'])
                # Do not save to mongo if already exists (previous runs)
                collection.update({'id':tweet['id']}, tweet, upsert=True)
                seenIds.add(tweet["id"])
                print('tweet ' + str(tweet['id']) + ' fetched,    total: ' + str(collection.estimated_document_count()))
            except Exception as e:
                print(e)
    # Wait a min till fetching next 10 tweets
    sleep(1)

data = json.loads(response.text)