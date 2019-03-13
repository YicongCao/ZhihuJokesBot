# coding=utf-8
import os
import pymongo
import random
import json

import push

from flask import Flask
from file2mongo import (client, collection, db)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/joke')
    def get_random_joke():
        count = collection.count()
        joke_bson = collection.find()[random.randrange(count)]
        # from bson.json_util import dumps
        # result = dumps(joke_bson)
        # return result
        joke_json = {
            "cover": joke_bson["cover"],
            "count": joke_bson["count"],
            "jokes": joke_bson["jokes"],
            "date": joke_bson["date"]
        }
        # return json.dumps(joke_json, indent=4, ensure_ascii=False)
        joke_md = push.generate_markdown_minimal(joke_json).strip()
        return joke_md

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
