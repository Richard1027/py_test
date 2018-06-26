# --*-- coding:utf8 --*--

import pymysql
import uuid
import time

from units.log import *
from units.config import Config


class Conn_DB:

    log = Logger().get_logger()

    def __init__(self):
        mysql_conf = Config().get('Mysql')
        self.host = mysql_conf.get('host')
        self.port = mysql_conf.get('port')
        self.user = mysql_conf.get('user')
        self.passwd = mysql_conf.get('passwd')
        self.dbname = mysql_conf.get('dbname')

    def _connect(self, charset="utf8"):

        if not self.dbname:
            raise (NameError, "not set the active db")

        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.passwd,
                                    db=self.dbname,
                                    charset=charset)

        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "connect to mysql failure")
        else:
            return cur

    def update(self, sql):
        try:
            with self._connect() as cur:
                res = cur.execute(sql)
                self.log.Info("The execute sql %s" % result)
                self.conn.commit()
            return res
        except Exception:
            self.conn.rollback()
            self.log.error("sql is empty or error %s" % sql)

    def insert(self, sql):
        try:
            with self._connect() as cur:
                res = cur.execute(sql)
                self.log.Info("The execute sql %s" % result)
                self.conn.commit()
            return res
        except Exception:
            self.conn.rollback()
            self.log.error("sql is empty or error %s" % sql)

    def delete(self, sql):
        try:
            with self._connect() as cur:
                res = cur.execute(sql)
                self.log.Info("The execute sql %s" % result)
                self.conn.commit()
            return res
        except Exception:
            self.conn.rollback()
            self.log.error("sql is empty or error %s" % sql)

    def select(self, sql):
        try:
            with self._connect() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result
                self.log.Info("The execute sql %s" % result)
        except Exception:
            self.log.error("sql is empty or error %s" % sql)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    c = Conn_DB()
    result = c.select("SELECT * FROM staff ")
    for record in result:
        print(record)