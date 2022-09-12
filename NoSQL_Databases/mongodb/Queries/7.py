import pymongo
from pymongo import MongoClient
import re
import time
from bson.code import Code 
# Set up mongo
client = MongoClient(username='root',
                     password='example')
db = client.sahamyab
collection = db.tweets



mapper = Code("function() {"
  " this.hashtags.forEach(function(z) {"
  "  emit(this.senderName, 1);" 
  "});" 
  "}")
var reduceFunction1 = function(keyCustId, valuesPrices) {
   return Array.sum(valuesPrices);
};
db.orders.mapReduce(
   mapFunction1,
   reduceFunction1,
   { out: "map_reduce_example" }
)