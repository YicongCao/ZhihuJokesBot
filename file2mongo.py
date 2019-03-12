# coding=utf-8
import pymongo
import glob
import os
import json
import random

import offline

DB_NAME = 'zhihu_jokes'
COLLECTION_NAME = 'papers'

client = pymongo.MongoClient('mongodb://localhost:27017/')
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


def test_joke_from_mongo():
    count = collection.count()
    return collection.find()[random.randrange(count)]


if __name__ == "__main__":
    do_file_to_mongo()
    print(test_joke_from_mongo())
