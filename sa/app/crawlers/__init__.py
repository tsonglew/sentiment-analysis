# -*- coding: utf-8 -*-

"""
    crawlers
    ----------------
    Toolbox:
        - Requests
        - BeatifulSoup

    Owner:
        - Kasheem Lew
"""

import os
import random

ua_path = os.getcwd().split('/')
ua_path.append("app/crawlers/user_agents.txt")
USER_AGENT_FILE = '/'.join(ua_path)


# Get a random User-Agent
def LoadUserAgents(uafile=USER_AGENT_FILE):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas
uas = LoadUserAgents()
ua = random.choice(uas)


# Config for Wuhan University Taoke
taoke_headers = {
        "Content-Type": "application/json",
        "Referer": "http://taoke.ziqiang.net.cn/",
        "X-CSRFToken": "75PLqppxh55CnegBhS1hyrGUAUZjmXlV",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "__utma=126494854.1217350532.1480563014.1480563014.1480563014.1; __utmc=126494854; __utmz=126494854.1480563014.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); csrftoken=75PLqppxh55CnegBhS1hyrGUAUZjmXlV"
        }
taoke_url = "http://taoke.ziqiang.net.cn/api/course/public/elective/"


# Config for Wuhan University of Technology Xuanxiuke
xuanxiuke_url = "http://xuan.wutnews.net/ajax/Comment_Data_More.ashx?PageType=index&CommentType=-1&click_more_num="

# Config for HUST ixuanxiu.com
first_page = "http://hust.ixuanxiu.hustonline.net/classify/"
second_page = "http://hust.ixuanxiu.hustonline.net/classify/science/"
third_page = "http://hust.ixuanxiu.hustonline.net/classify/mixed/"
ixuanxiu_url = "http://hust.ixuanxiu.hustonline.net/comment/all/"
