# -*- coding: utf-8 -*-

"""
    Part III of crawler. Ixuanxiu of HUST
"""

import requests
from app import db
from bs4 import BeautifulSoup
from ..models import Comment
from . import first_page, second_page, third_page, ixuanxiu_url


def handle_page(url, count):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    uls = soup.find_all('ul', class_="clearfix")

    # handle each container
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            try:
                href = li.a['href']
                no = href.split('/')[2]

                # handle second pages
                second_url = "".join([ixuanxiu_url, no])
                second_r = requests.get(second_url)
                second_soup = BeautifulSoup(second_r.text, "lxml")
                all_firstchild = second_soup.find_all('li', class_="firstchild")
                for firstchild in all_firstchild:
                    comment = firstchild.find_next_sibling('li').text
                    c = Comment(
                            body = comment,
                            emotion = 0
                            )
                    db.session.add(c)
                    print "No.%03d Comment into Database!" % count
                    count += 1

            except TypeError:
                pass

    db.session.commit()
    return count


def ixuanxiu():
    print "Getting Response from %r ..." % ixuanxiu_url

    count = 0
    a_count = handle_page(first_page, count)
    b_count = handle_page(second_page, a_count)
    c_count = handle_page(third_page, b_count)

    print "%d Courses From HUST Ixuanxiu Handled!" % c_count
