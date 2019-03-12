# coding=utf-8

import requests
import json
import datetime
import time

import utils

DAILY_NEWS_API = "http://news-at.zhihu.com/api/4/news/latest"
JOKES_SECTION_API = "http://news-at.zhihu.com/api/4/section/2"
JOKES_HISTORY_API = "http://news-at.zhihu.com/api/4/section/2/before/{0}"
JOKES_ARTICLE_URL = "http://daily.zhihu.com/story/{0}"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'
}

JOKE_ID_FILENAME = 'joke_id'
JOKE_DATE_FILENAME = 'joke_date'


def get_html_from_url(url):
    if None == url:
        return None
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("open {0} failed".format(url))
        return None
    return r.text


def get_today_joke_url():
    r = requests.get(DAILY_NEWS_API, headers=HEADERS)
    if r.status_code != 200:
        print("invoke DAILY_NEWS_API failed")
        return None
    daily_json = json.loads(r.text)
    for story in daily_json['stories']:
        if "瞎扯" in story['title'] or "如何正确地吐槽" in story['title']:
            return JOKES_ARTICLE_URL.format(story['id'])
    return None


def get_history_joke_url_list():
    cur_section_html = get_html_from_url(JOKES_SECTION_API)
    if None == cur_section_html:
        print("cur_section_html is None")
        return None

    def parse_section_json(sec_html):
        sec_json = json.loads(sec_html)
        if 'timestamp' not in sec_json:
            return None, [], []
        joke_id_sub_list = []
        date_sub_list = []
        for story in sec_json['stories']:
            joke_id_sub_list.append(story['id'])
            date_sub_list.append(story['date'])
        return sec_json['timestamp'], joke_id_sub_list, date_sub_list

    utils.clear_list_to_text(JOKE_ID_FILENAME)
    utils.clear_list_to_text(JOKE_DATE_FILENAME)
    joke_id_total_list = []
    date_total_list = []
    timestamp, joke_id_list, date_list = parse_section_json(cur_section_html)
    joke_id_total_list.extend(joke_id_list)
    while None != timestamp and len(joke_id_list) > 0:
        cur_section_html = get_html_from_url(
            JOKES_HISTORY_API.format(timestamp))
        if None == cur_section_html:
            print("cur_section_html got None")
            break
        timestamp, joke_id_list, date_list = parse_section_json(
            cur_section_html)
        if None == timestamp:
            print("encounters no data")
            break
        joke_id_total_list.extend(joke_id_list)
        date_total_list.extend(date_list)
        dt_hist = datetime.datetime.fromtimestamp(timestamp)
        print("got {0} jokes dates back to {1}-{2}-{3}, have {4} jokes total".format(len(
            joke_id_list), dt_hist.year, dt_hist.month, dt_hist.day, len(joke_id_total_list)))
        joke_url_list = [JOKES_ARTICLE_URL.format(id) for id in joke_id_list]
        utils.save_list_to_text(JOKE_ID_FILENAME, joke_url_list)
        utils.save_list_to_text(JOKE_DATE_FILENAME, date_list)
        # time.sleep(0.01)
    return joke_id_total_list


if __name__ == "__main__":
    # print(get_html_from_url(get_today_joke_url()))
    get_history_joke_url_list()
