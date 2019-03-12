# coding=utf-8

import json
import requests
import time

import push
import spider
import utils

pushed = False


def do_push():
    ori_url = spider.get_today_joke_url()
    myhtml = spider.get_html_from_url(ori_url)
    if None == myhtml:
        print("spider failed")
    myjokes = utils.get_qa_from_html(myhtml)
    if None == myjokes:
        print("parse failed")
    rtx_md = push.generate_rtx_markdown(myjokes)
    rtx_card = push.generate_rtx_cardinfo(myjokes, ori_url)
    push.push_to_rtx(rtx_card)
    push.push_to_rtx(rtx_md)


def timer_func():
    global pushed
    if utils.check_if_is_time(7, 30) and not pushed:
        pushed = True
        do_push()
        import os
        os._exit(0)
        return True
    return False


def timer_test_func():
    print('timer')


if __name__ == "__main__":
    while True:
        print(utils.get_date_str() + " " + utils.get_time_str())
        timer_func()
        time.sleep(30)
