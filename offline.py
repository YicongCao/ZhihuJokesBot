# coding=utf-8
import requests
import json
import os
import time

import spider
import utils
import push

OFFLINE_DIR = "jokes_offline"

if __name__ == "__main__":
    # write joke id list to file
    # spider.get_history_joke_url_list()
    # load joke id list from file
    joke_url_list = utils.load_list_from_text(spider.JOKE_ID_FILENAME)
    joke_date_list = utils.load_list_from_text(spider.JOKE_DATE_FILENAME)
    for joke_url, joke_date in zip(joke_url_list, joke_date_list):
        joke_url = str(joke_url).strip()
        joke_date = str(joke_date).strip()
        # skip saved ones
        if os.path.isfile("./{0}/{1}.json".format(OFFLINE_DIR, joke_date)):
            continue

        print("getting " + joke_url)
        myhtml = spider.get_html_from_url(joke_url)
        if None == myhtml:
            print("get html failed")
            continue
        myjokes = utils.get_qa_from_html(myhtml)
        if None == myjokes:
            print("parse failed")
            continue
        joke_md = push.generate_markdown(myjokes)
        joke_json = json.dumps(myjokes, indent=4, ensure_ascii=False)
        filename = joke_date
        with open("./{0}/{1}.md".format(OFFLINE_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(joke_md.strip())
        with open("./{0}/{1}.json".format(OFFLINE_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(joke_json)
        time.sleep(0.01)
