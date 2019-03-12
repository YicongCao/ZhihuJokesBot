# coding=utf-8

import json
import spider
import utils
import requests

RTX_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d79c6373-d966-426f-9736-0baf8ecff172"
RTX_WEBHOOK_URL_FOR_TEST = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fb99373d-bd25-40d3-803d-64997f84df1b"
MD_HEADER = """
## 如何正确地吐槽

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
    r = requests.post(RTX_WEBHOOK_URL_FOR_TEST, json=msg_json)
    print(r.text + "\r\n")
    print(r.status_code, r.reason, "\r\n\r\n")


def generate_markdown(jokes_json):
    if None == jokes_json:
        print("jokes_json is None")
        return None
    md_bodys = []
    for joke in jokes_json['jokes']:
        md_body = ""
        # body add ref syntax
        content = joke['content']
        content = "> " + \
            "\r\n> ".join(list(filter(None, content.split("\r\n"))))
        joke['content'] = content
        md_body += (MD_BODY.format(**joke))
        for img in joke['imgs']:
            md_body += MD_IMGS.format(**{"img": img})
        md_body += MD_FOOT.format(**joke)
        md_bodys.append(md_body)
    md_result = MD_HEADER + " \r\n---\r\n" + "\r\n---\r\n".join(md_bodys)
    print(md_result)
    return md_result


def generate_rtx_markdown(jokes_json):
    md_content = generate_markdown(jokes_json)
    data = {}
    data['msgtype'] = 'markdown'
    data['markdown'] = {}
    data['markdown']['content'] = md_content
    print(data)
    return data


def generate_rtx_cardinfo(jokes_json, ori_url):
    if None == jokes_json:
        print("jokes_json is None")
        return None
    articles = []
    articles.append({
        'title': '今日份的沙雕',
        'url': ori_url,
        'picurl': jokes_json['cover'],
        'description': '今天是 ' + utils.get_date_str()
    })
    data = {}
    data['msgtype'] = 'news'
    data['news'] = {}
    data['news']['articles'] = articles
    print(data)
    return data


if __name__ == "__main__":
    # ori_url = spider.get_today_joke_url()
    ori_url = "http://daily.zhihu.com/story/9707327"
    myhtml = spider.get_html_from_url(ori_url)
    if None == myhtml:
        print("spider failed")
    myjokes = utils.get_qa_from_html(myhtml)
    if None == myjokes:
        print("parse failed")
    rtx_md = generate_rtx_markdown(myjokes)
    rtx_card = generate_rtx_cardinfo(myjokes, ori_url)
    push_to_rtx(rtx_card)
    push_to_rtx(rtx_md)
