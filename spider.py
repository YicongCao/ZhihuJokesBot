# coding=utf-8

import requests
import json

DAILY_NEWS_API = "http://news-at.zhihu.com/api/4/news/latest"
JOKES_SECTION_API = "http://news-at.zhihu.com/api/4/section/2"
JOKES_HISTORY_API = "http://news-at.zhihu.com/api/4/section/2/before/{0}"
JOKES_ARTICLE_URL = "http://daily.zhihu.com/story/{0}"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'
}


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


if __name__ == "__main__":
    print(get_html_from_url(get_today_joke_url()))
