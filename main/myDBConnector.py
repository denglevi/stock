# coding=utf-8
import MySQLdb


class MyDBConnector:
    host = '127.0.0.1'
    username = 'root'
    password = ''
    db = 'stock2'
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(
            user=self.username,
            passwd=self.password,
            host=self.host,
            db=self.db
        )
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def execSql(self,sql):

        return self.cursor.excute(sql)

    def getData(self,sql):
        self.cursor.execute(sql)

        return self.cursor.fetchall()
