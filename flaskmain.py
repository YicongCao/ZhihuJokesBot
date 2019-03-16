# coding=utf-8
import os
import pymongo
import random
import json

import file2mongo
import push

from flask import (Flask, request)
from file2mongo import (client, collection, db)
from werkzeug.exceptions import abort


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/joke')
    def get_random_joke():
        # count = collection.count()
        # print('total jokes count: ', count)
        # joke_bson = collection.find()[random.randrange(count)]
        joke_bson = file2mongo.random_joke_from_mongo()
        # from bson.json_util import dumps
        # result = dumps(joke_bson)
        # return result
        joke_json = {
            "cover": joke_bson["cover"],
            "count": joke_bson["count"],
            "jokes": joke_bson["jokes"],
            "date": joke_bson["date"]
        }
        print(joke_json)
        # return json.dumps(joke_json, indent=4, ensure_ascii=False)
        joke_md = push.generate_markdown_minimal(joke_json).strip()
        return joke_md

    @app.route('/jokedict')
    def get_query_joke():
        keyword = request.args.get('keyword')
        if keyword == None or len(keyword) == 0:
            abort(401)
        joke_bson = file2mongo.query_joke_from_mongo(keyword)
        found = True
        if None == joke_bson:
            found = False
            joke_bson = file2mongo.random_joke_from_mongo()
            # count = collection.count()
            # print('total jokes count: ', count)
            # joke_bson = collection.find()[random.randrange(count)]
        joke_json = {
            "cover": joke_bson["cover"],
            "count": joke_bson["count"],
            "jokes": joke_bson["jokes"],
            "date": joke_bson["date"]
        }
        print(joke_json)
        if not found:
            keyword = None
        joke_md = push.generate_markdown_minimal(
            joke_json, contains=keyword).strip()
        return joke_md

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
