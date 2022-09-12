
import pymongo
from pymongo import MongoClient
import re

# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets

collection.aggregate([
	{ "$addFields": {
		'hashtags': { '$regexFindAll': { 'input': "$content", 'regex': r"#(\w+)"}} }},
	{ '$set': { 'hashtags': "$hashtags.match"}},
	{ "$out": "temp" }
	])

for i in db.temp.find({}):
    if i['hashtags']:
          print(i['hashtags'])
