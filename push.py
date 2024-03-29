# coding=utf-8

import json
import spider
import utils
import requests
import random

RTX_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d79c6373-d966-426f-9736-0baf8ecff172"
RTX_WEBHOOK_URL_FOR_TEST = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d799e324-dcc7-4bfb-907f-1acce7263464"
SAND_WEBHOOK_URL = "http://9.66.10.155:31112/function/pushbotgo"
MD_HEADER = """
## 今日份的沙雕

> 看点好段子，有个好心情～


"""
MD_BODY = """
### {title}

{content}

"""
MD_IMGS = """

![配图]({img})

"""
MD_FOOT = """
作者：`{author}`
"""


def push_to_rtx(msg_json):
    print('\r\nposting to rtx...')
    r = requests.post(RTX_WEBHOOK_URL, json=msg_json)
    print(r.text + "\r\n")
    print(r.status_code, r.reason, "\r\n\r\n")


def push_to_sand(msg_json):
    print('\r\nposting to sand...')
    r = requests.post(SAND_WEBHOOK_URL, json=msg_json)
    print(r.text + "\r\n")
    print(r.status_code, r.reason, "\r\n\r\n")


def generate_markdown_minimal(jokes_json, contains=None):
    md_bodys = []
    if None == contains:
        joke = jokes_json['jokes'][random.randrange(len(jokes_json['jokes']))]
        if len(joke['imgs']) > 0:
            joke = jokes_json['jokes'][random.randrange(
                len(jokes_json['jokes']))]
    else:
        for j in jokes_json['jokes']:
            if contains in j['content']:
                joke = j
                break
    md_body = ""
    # body add ref syntax
    tempjoke = {
        "title": joke['title'],
        "author": joke['author'],
        "bio": joke['bio'],
        "imgs": joke['imgs'],
        "content": joke['content']
    }
    content = joke['content']
    content = "> " + \
        "\r\n> \r\n> ".join(list(filter(None, content.split("\r\n"))))
    tempjoke['content'] = content
    md_body += (MD_BODY.format(**tempjoke))
    for img in tempjoke['imgs']:
        md_body += MD_IMGS.format(**{"img": img})
    md_body += MD_FOOT.format(**tempjoke)
    md_bodys.append(md_body)
    md_result = "\r\n---\r\n".join(md_bodys)
    return md_result


def generate_markdown(jokes_json):
    if None == jokes_json:
        print("jokes_json is None")
        return None
    md_bodys = []
    for joke in jokes_json['jokes']:
        md_body = ""
        # body add ref syntax
        content_bak = joke['content']
        content = joke['content']
        content = "> " + \
            "\r\n> \r\n> ".join(list(filter(None, content.split("\r\n"))))
        joke['content'] = content
        md_body += (MD_BODY.format(**joke))
        for img in joke['imgs']:
            md_body += MD_IMGS.format(**{"img": img})
        md_body += MD_FOOT.format(**joke)
        md_bodys.append(md_body)
        joke['content'] = content_bak
    md_result = MD_HEADER + " \r\n---\r\n" + "\r\n---\r\n".join(md_bodys)
    # print(md_result)
    return md_result


def generate_sand_markdown(jokes_json):
    md_content = generate_markdown(jokes_json)
    push_body = {
        "msgtype": 23,
        "botid": "82a4f129-7d73-4d48-8623-b153e2d4ca5c",
        "msgbody": md_content
    }
    print(push_body)
    return push_body


def generate_rtx_markdown(jokes_json):
    md_content = generate_markdown(jokes_json)
    data = {}
    data['msgtype'] = 'markdown'
    data['markdown'] = {}
    data['markdown']['content'] = md_content
    print(data)
    return data


def generate_rtx_cardinfo(jokes_json, ori_url, today=True):
    if None == jokes_json:
        print("jokes_json is None")
        return None
    articles = []
    if today:
        articles.append({
            'title': '如何正确地吐槽',
            'url': ori_url,
            'picurl': jokes_json['cover'],
            'description': '今天是 ' + utils.get_date_str()
        })
    else:
        articles.append({
            'title': '往期沙雕',
            'url': ori_url,
            'picurl': jokes_json['cover']
        })
    data = {}
    data['msgtype'] = 'news'
    data['news'] = {}
    data['news']['articles'] = articles
    print(data)
    return data


if __name__ == "__main__":
    ori_url = spider.get_today_joke_url()
    # ori_url = "http://daily.zhihu.com/story/9670542"
    myhtml = spider.get_html_from_url(ori_url)
    if None == myhtml:
        print("spider failed")
    myjokes = utils.get_qa_from_html(myhtml)
    if None == myjokes:
        print("parse failed")
    rtx_md = generate_rtx_markdown(myjokes)
    rtx_card = generate_rtx_cardinfo(myjokes, ori_url, today=True)
    push_to_rtx(rtx_card)
    push_to_rtx(rtx_md)
    sand_md = generate_sand_markdown(myjokes)
    push_to_sand(sand_md)
