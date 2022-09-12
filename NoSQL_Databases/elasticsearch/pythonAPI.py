import requests
from elasticsearch import Elasticsearch
import re
import time 

url = 'https://www.sahamyab.com/guest/twiter/list?v=0.1'
elasticSearch = Elasticsearch([{'host': 'localhost', 'port': 9200}])
total = 1000
fetched = 0
seenIds = set()
hashtags = list()

while fetched < total:
    response = requests.get(url=url, headers={'User-Agent': 'Chrome/61', 'Connection': 'Close'})
    if response.status_code != 200:
        print('HTTP', response.status_code)
        continue
    
    data = response.json()["items"] # Check the JSON Response Content documentation bellow
    for tweet in data:
        if tweet["id"] not in seenIds:
            try:
                tweet["hashtags"] = re.findall(r'#(\w+)', tweet['content'])
                #tweet.pop('key', None)
                elasticSearch.index(index='twitter', doc_type='twitter', body=tweet)
                seenIds.add(tweet["id"])
                fetched += 1
                print('tweet ' + str(tweet['id']) + ' fetched,    total: ' + str(fetched))
            except Exception as e:
                print(e)