# -*- coding:utf-8 -*-
# Author:lixuecheng

import pymysql
from requestQ.package.logger import log, logger
from requestQ.package.baseClass import baseClass


class DoMysql(baseClass):
    @log
    def __init__(self, ip, user, password, dbname, port=3306, is_autocommit=True):
        self.req = {'db': {'ip': ip, 'port': port, 'user': user,
                           'password': password[0:1]+'*****'+password[-1:], 'db': dbname}}
        self.status = True
        self.res = {}
        self.e = ''

        try:
            self.ip = ip
            self.user = user
            self.passwd = password
            self.dbname = dbname
            self.port = port
            self.db = pymysql.connect(host=ip, port=int(port), user=user, password=password,
                                      database=dbname, charset='utf8', autocommit=False)
            self.string = ip + ':' + \
                str(port) + ',user=' + user + ',password=' + \
                password + ',database=' + dbname
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            self.is_auto = is_autocommit

            logger.info('mysql连接成功，-----' + self.string)
        except Exception as e:
            self.db = None
            self.cursor = False
            self.e = '数据库连接失败：' + str(e)
            self.string = str(e)
            self.status = False
            # raise Exception('数据库连接失败：' + str(e))

    def __str__(self):
        try:
            return 'mysql_' + self.string
        except Exception as e:

            # logger.warn('mysql字符串转化失败，' + str(e))
            return 'mysql,无字符串初始化，获取是日志获取中发生,' + str(e)
            # raise Exception('mysql字符串转化失败，' + str(e))

    @log
    def run(self, sql: str) -> int:

        if self.cursor:
            try:
                self.req['sql'] = sql
                self.cursor.execute(sql)

                self.res['data'] = self.cursor.fetchall()

                if self.is_auto:
                    self.commit()
                self.res['rowcount'] = self.cursor.rowcount
                self.status = True

                return self.cursor.rowcount
            except Exception as e:
                self.e = sql+',执行sql失败，' + str(e)
                self.status = False
        else:
            self.status = False
            return 0

    def close(self):

        try:
            self.cursor.close()
            self.db.close()
        except:
            pass
        self.status = False

    def commit(self):
        
        logger.info('执行数据库提交')
        self.db.commit()

    def rollback(self):
   
        logger.info('执行数据库回滚,' + str(self.e))
        self.db.rollback()


# try:
# aa = DoMysql('172.16.9.28', 'root', 'a111111', '')

# print(aa.run('SHOW DATABASES'))
#     # raise Exception('')
#     aa.commit()
# except:
#     aa.rollback()
# aa = DoMysql('172.16.9.28', 'root', 'a111111', 'gtobusinessdb')
# a=aa.run('SELECT * from am_resign ')
# print(a)
