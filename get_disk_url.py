import webbrowser
import time
import common
from pyquery import PyQuery as pq
from db import db_connect

# 连接数据库
db, cur = db_connect()

'''
2 根据电影数据列表movie,通过panduoduo 搜索出能播放的百度云资源
'''


# pq语法获取信息
def get_list(html):
    doc = pq(html)
    content = doc(".container .search-page .row")
    return content


# 如不存在插入百度云资源
def insert_source(**data):
    cur.execute("insert into source(url,ref_id,movie_id) values(%s, %s, %s)",
                (data['url'], data['ref_id'], data['movie_id']))
    db.commit()
    last_id = cur.lastrowid
    return last_id


# 根据id搜索对应的百度云资源
def get_souce(id, movie_id):
    # 如果已存在则不搜索
    sql = "select * from source where ref_id=%s"  # %s需要去掉引号，pymysql会自动加上
    cur.execute(sql, [id])
    row = cur.fetchone()
    if (row):
        return 0

    page_url = "http://pdd.19mi.net/go/" + str(id)
    response = common.set_url(page_url, headers=common.header)
    # response = set_url("http://pdd.19mi.net/go/50720920", headers=header)
    if (response):
        if (response.status_code != 200):
            return 0
        doc = pq(response.text)
        url = doc("a").attr("href")

        if not url:
            print(page_url, " no url")
            webbrowser.open(page_url)

            # 如果弹出要输入验证码, 输入后控制台按enter继续
            input("input the verify code then enter to continue")
            # exit("check code")
            return 0

        response = common.set_url(url, headers=common.header)
        doc = pq(response.text)
        content = doc("#bd-main")

        if content:
            insert_data = {}
            insert_data['url'] = url
            insert_data['ref_id'] = id
            insert_data['movie_id'] = movie_id
            insert_id = insert_source(**insert_data)
            return insert_id
        else:
            return 0
    else:
        return 0


#################### start ######################
#cur.execute('select * from movie order by id DESC')
# 指定id
cur.execute('select * from movie where id=37')
rows = cur.fetchall()

for row in rows:

    movie_id = row['id']

    response = common.set_url("http://www.panduoduo.net/s/name/" + row['title'], headers=common.header)
    doc_ob = get_list(response.text)
    count = 0
    for item in doc_ob.items():  # 使用items()可以保留结果的pyjuery对象
        time.sleep(1)
        url = item("h3 a").attr("href")
        code = url.split("/")
        id = code[-1].strip()
        insert_id = get_souce(id, movie_id)
        if insert_id > 0:
            count += 1
            print("insert new record", insert_id)
            time.sleep(10)

print("insert record:", count)
