import time
import common
from pyquery import PyQuery as pq
from db import db_connect

db, cur = db_connect()

'''
1 获取豆瓣前250电影的电影列表
'''


# pq语法获取信息
def get_list(html):
    doc = pq(html)
    content = doc("#content ol li")
    return content


# 如不存在插入电影数据
def insert_movie(**data):
    sql = "select * from movie where ref_id=%s"  # %s需要去掉引号，pymysql会自动加上
    cur.execute(sql, [data['ref_id']])
    row = cur.fetchone()
    if (row):
        return 0

    cur.execute("insert into movie(url,img,title,star,quote,ref_id,create_time) values(%s, %s,  %s,  %s, %s, %s, %s)",
                (data['url'], data['img'], data['title'], data['star'], data['quote'], data['ref_id'],
                 data['create_time']))
    db.commit()
    last_id = cur.lastrowid
    return last_id


#################### start 1 ######################
# 当前页数,默认为1
page = 1
start = 25 * (page - 1)

params = {
    "start": start
}

response = common.set_url("https://movie.douban.com/top250", headers=common.header, params=params)
doc_ob = get_list(response.text)

count = 0
for item in doc_ob.items():  # 使用items()可以保留结果的pyjuery对象
    insert_data = {}
    insert_data['url'] = item(".pic a").attr("href")
    insert_data['img'] = item(".pic img").attr("src")
    insert_data['title'] = item(".pic img").attr("alt")
    insert_data['star'] = item(".info .star .rating_num").text()
    insert_data['quote'] = item(".quote .inq").text()
    insert_data['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    code = insert_data['url'].split("/")
    insert_data['ref_id'] = code[-2].strip()

    insert_id = insert_movie(**insert_data)
    if insert_id > 0:
        count += 1
    # cur.execute("insert into movie(url,img,title,star,quote,ref_id,create_time) values(%s, %s,  %s,  %s, %s, %s, %s)",(url, img,title,star,quote,id,create_time))
    # db.commit()

print("insert record:", count)

