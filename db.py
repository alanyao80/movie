import pymysql

#数据库连接
def db_connect():
    db = pymysql.connect(host='localhost', user='root', passwd='11111111', db='test',cursorclass = pymysql.cursors.DictCursor)
    cur = db.cursor()
    return db,cur