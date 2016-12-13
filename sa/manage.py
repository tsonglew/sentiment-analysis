# -*- coding: utf-8 -*-

import sys
import os
from emo_list import pos_list, neg_list
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import db, app
from app.models import User, Role, Comment

# 编码设置
reload(sys)
sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
        Role = Role,
        Comment = Comment
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """run your unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def admin():
    """add administrator"""
    from getpass import getpass
    username = raw_input("\_admin username: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print "<admin user %s add in database>" % username


@manager.command
def adduser():
    """add user"""
    from getpass import getpass
    username = raw_input("\_username: ")
    email = raw_input("\_email: ")
    role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
    password = getpass("\_password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = role_id
    )
    db.session.add(u)
    db.session.commit()
    print "<user %s add in database>" % username


@manager.command
def crawler():
    """crawler"""
    print "Uncomment the utilities to start the crawler!"
    from app.crawlers.taoke import taoke
    taoke()

    from app.crawlers.ixuanxiu import ixuanxiu
    ixuanxiu()

    from app.crawlers.xuanxiuke import xuanxiuke
    xuanxiuke()


@manager.command
def parse():
    """parse the comments"""
    import jieba
    import jieba.posseg as pseg

    # Load User's Dictionary
    path_list = os.getcwd().split('/')
    path_list.append("dict.txt")
    dict_path = '/'.join(path_list)
    jieba.load_userdict(dict_path)

    # Disimss These Flags
    dismiss = ['b', 'c', 'r', 'uj', 'u', 'p', 'q', 'uz', 't', 'ul', 'k', 'f',
            'ud', 'ug', 'uv']

    comments = Comment.query.all()
    for comment in comments:
         word_list = []
         pseg_cut = pseg.cut(comment.body)
         for word, flag in pseg_cut:
             if flag not in dismiss:
                 word_list.append(word)
         comment.parsed = '/'.join(word_list)
         db.session.add(comment)
         print "Comment %04d Parsed!" % comment.id

    db.session.commit()
    print "ALL DONE!"


@manager.command
def get_count():
    comments = Comment.query.all()
    for comment in comments:
        for word in comment.parsed.split('/'):
            if word in pos_list:
                comment.pos_count += 1
            elif word in neg_list:
                comment.neg_count += 1
            elif '80' <= word and word <= '99':
                comment.pos_count += 1
            elif '0' <= word and word < '80':
                comment.neg_count += 1
        db.session.add(comment)
        print "Comment %04d counted!" % comment.id
    db.session.commit()
    print "ALL DONE!"


@manager.command
def get_theta():
    import math
    theta = [0.0, 0.0, 0.0]
    step = 0.01
    comments = Comment.query.all()[:100]
    print "Comments gotten! Training..."
    for m in range(1000):
        for comment in comments:
            if comment.emotion != -1:
                x = [1, float(comment.pos_count), float(comment.neg_count)]
                feature_sum = 0
                for i in range(3):
                    feature_sum += theta[i]*x[i]

                h = 1 / (1+math.e**-(feature_sum))
                for i in range(3):
                    theta[i] = theta[i] + step*(comment.emotion-h)*x[i]
    print "Theta Gotten: ", theta


@manager.command
def get_emotion():
    print "Calculating thetas..."
    get_theta()
    print "Done!"
    comments = Comment.query.filter_by(emotion=-1).all()
    for comment in comments:
        x = [1, float(comment.pos_count), float(comment.neg_count)]
        hypothesis = 0
        feature_sum = 0
        for i in range(3):
            feature_sum += theta[i]*x[i]
        hypothesis = 1 / (1+math.e**-(feature_sum))
        if 0 < hypothesis < 0.4:
            comment.analysis_score = 0
        elif 0.4 <= hypothesis < 0.6:
            comment.analysis_score = 0.5
        elif 0.6 <= hypothesis < 1:
            comment.analysis_score = 1


if __name__ == '__main__':
    manager.run()

