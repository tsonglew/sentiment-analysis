# -*- coding: utf-8 -*-

"""
    Part I of crawler. Taoke of Wuhan University
"""

import requests
from app import db
from . import taoke_url, taoke_headers
from ..models import Comment


def taoke():
    print "Getting Response from %r ..." % taoke_url,
    r = requests.post(taoke_url, headers=taoke_headers)

    if r:
        print "\b\b\bDone!"
    else:
        print "\b\b\bError!"
        return ""

    classes = r.json()['public_elective']
    classes_no = []
    for each_class in classes:
        classes_no.append(each_class['number'])

    for each_no in classes_no:
        print "Checking on Course  %11d ..." % each_no,
        cls_r = requests.get("".join([taoke_url, "%d"%each_no, "/comment/"]))
        comments = cls_r.json()['comment']
        comment_count = 0
        for each_comment in comments:
            content = each_comment['content']
            c = Comment(
                    body = content,
                    emotion = 0
                    )
            db.session.add(c)
            db.session.commit()
            comment_count += 1
        print "\b\b\b\b\b %d comments handled" % comment_count

    print "All Courses From Wuhan University Taoke Handled!"
