# coding=utf-8
import pymongo
import glob
import os
import json
import random

import offline

DB_NAME = 'zhihu_jokes'
COLLECTION_NAME = 'papers'

#client = pymongo.MongoClient(host='localhost', port=27017)
#client = pymongo.MongoClient(host='db', port=27017)
client = pymongo.MongoClient(host='mongodb.botplatform', port=8080)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def do_file_to_mongo():
    for infile in glob.glob("./{0}/*.json".format(offline.OFFLINE_DIR)):
        folder, fullname = os.path.split(infile)
        filename, extension = os.path.splitext(fullname)
        with open(infile, 'r', encoding='utf-8') as f:
            jokes_json_str = f.read()
            jokes_json = json.loads(jokes_json_str)
            jokes_json['date'] = filename
            collection.insert_one(jokes_json)


def random_joke_from_mongo():
    count = collection.count()
    return collection.find()[random.randrange(count)]


def query_joke_from_mongo(keyword):
    jokes = collection.find(
        {
            'jokes.content':
            {
                '$regex': ".*{0}.*".format(keyword)
            }
        })
    count = jokes.count()
    if count == 0:
        return None
    return jokes[random.randrange(count)]


if __name__ == "__main__":
    do_file_to_mongo()
    print(query_joke_from_mongo('下楼'))
