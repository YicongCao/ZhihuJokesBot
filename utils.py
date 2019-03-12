# coding=utf-8
import os
import codecs
import csv
import json
from bs4 import BeautifulSoup


def get_qa_from_html(html_text):
    if None == html_text:
        print('html_text is None')
        return None
    soup = BeautifulSoup(html_text, 'html.parser', from_encoding='utf-8')
    if None == soup:
        print('soup parse failed')
        return None
    # find cover img
    cover_parent = soup.find_all('h1', class_="headline-title")
    for cover_parent_sub in cover_parent:
        img = cover_parent_sub.find_next('img')
        cover = img.attrs['src']
    # find articles
    questions = soup.find_all('div', class_="question")
    if None == questions:
        print('soup find no questions')
        return None
    jokes = []
    for question in questions:
        title = ""
        for h2 in question.find_all('h2', class_="question-title"):
            title = h2.text
        for answer in question.find_all('div', class_="answer"):
            author = ""
            bio = ""
            paras = []
            content = ""
            imgs = []
            for span in answer.find_all('span', class_="author"):
                author = span.text
            for span in answer.find_all('span', class_="bio"):
                bio = span.text
            for cnt in answer.find_all('div', class_="content"):
                for p in cnt.find_all('p'):
                    paras.append(p.text)
                for img in cnt.find_all('img', class_="content-image"):
                    imgs.append(img.attrs['src'])
            content = "\r\n".join(paras)
            # remove multiple \r\n
            content = "\r\n".join(list(filter(None, content.split("\r\n"))))
            author = str(author).replace("，", "")
            jokes.append({
                "title": title,
                "author": author,
                "bio": bio,
                "imgs": imgs,
                "content": content
            })
    ret_json = {
        "cover": cover,
        "count": len(jokes),
        "jokes": jokes
    }
    return ret_json


def get_date_str():
    import calendar
    import datetime
    d = datetime.datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    weekday_str = weekdays[d.weekday()]
    date_str = "{0}-{1}-{2}".format(d.year, d.month, d.day)
    return date_str + " " + weekday_str


def get_time_str():
    import datetime
    d = datetime.datetime.now()
    time_str = "{0}:{1}:{2}".format(d.hour, d.minute, d.second)
    return time_str


def check_if_is_time(hour, minute):
    import datetime
    d = datetime.datetime.now()
    if d.hour == hour and d.minute == minute:
        return True
    else:
        return False


def clear_list_to_text(filename):
    file = open(str(filename) + ".txt", 'w', encoding='utf-8')
    file.close()


def save_list_to_text(filename, id_list):
    with open(str(filename) + ".txt", 'a', encoding='utf-8') as f:
        for id in id_list:
            f.write(str(id) + "\r\n")


def load_list_from_text(filename):
    with open(str(filename) + ".txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines


if __name__ == "__main__":
    import sys
    import io
    import spider
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # myhtml = spider.get_html_from_url(spider.get_today_joke_url())
    myhtml = spider.get_html_from_url("http://daily.zhihu.com/story/9707327")
    if None == myhtml:
        print("spider failed")
    print(get_qa_from_html(myhtml))
