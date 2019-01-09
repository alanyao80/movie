import time
import common
from pyquery import PyQuery as pq
from db import db_connect

db, cur = db_connect()

'''
根据网址获取豆瓣指定电影信息
'''


# pq语法获取信息
def get_detail(html):
    doc = pq(html)
    content = doc("#content")
    return content


# 如不存在插入电影数据
def insert_movie(**data):
    sql = "select * from movie where ref_id=%s"  # %s需要去掉引号，pymysql会自动加上
    cur.execute(sql, [data['ref_id']])
    row = cur.fetchone()
    if (row):
        print("the record have been inserted, id=",row['id'])
        exit()
        #return 0

    cur.execute("insert into movie(url,img,title,star,quote,ref_id,create_time) values(%s, %s,  %s,  %s, %s, %s, %s)",
                (data['url'], data['img'], data['title'], data['star'], data['quote'], data['ref_id'],
                 data['create_time']))
    db.commit()
    last_id = cur.lastrowid
    return last_id


#################### start 1 ######################

# 指定网址
url = "https://movie.douban.com/subject/25761178/"
response = common.set_url(url, headers=common.header)
item = get_detail(response.text)

insert_data = {}
insert_data['url'] = url
insert_data['img'] = item("#mainpic img").attr("src")
long_title = item("h1 span").text()
code = long_title.split(" ")
title = code[0].strip()  #只除前面中文标题
insert_data['title'] = title
insert_data['star'] = item("#interest_sectl .rating_self strong").text()
insert_data['quote'] = ''
insert_data['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
code = insert_data['url'].split("/")
insert_data['ref_id'] = code[-2].strip()

insert_id = insert_movie(**insert_data)
if insert_id > 0:
    print("insert new record id=", insert_id)
else:
    print("insert fail")

