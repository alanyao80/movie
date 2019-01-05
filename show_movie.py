import common
from db import db_connect

db, cur = db_connect()

'''
3 打印指定movie可看百度云资源
'''

#################### start ######################

cur.execute('select m.id,m.title,m.star,s.url as disk_url from movie m left join source s on (m.id = s.movie_id) where m.id=31')
rows = cur.fetchall()

for row in rows:
    print(row)