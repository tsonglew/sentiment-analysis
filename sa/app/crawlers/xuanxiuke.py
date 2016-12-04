# -*- coding: utf-8 -*-

"""
    Part II of crawler. Xuanxiuke of Wuhan University of Technology
"""

import time
import requests
from app import db
from bs4 import BeautifulSoup
from ..models import Comment
from . import xuanxiuke_url


if xrange:
    range = xrange


def xuanxiuke():
    count = 0
    for i in range(144):
        if (i+1) % 50 == 0:
            time.sleep(10)
        r = requests.post("".join([xuanxiuke_url, "%d" % i]))
        r_rows = r.json()['rows']

        for each_row in r_rows:
            comment = each_row['JSON_commentcontent']
            print comment
            c = Comment(
                    body = comment,
                    emotion = 0
                    )
            db.session.add(c)
            count += 1
            print i
            print "No.%3d Course Handled!" % count
    db.session.commit()
