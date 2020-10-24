import pymysql
import config.database as database
import re
import config.dmlpro as dml
import config.sql as  configsql


class MysqlInsertTuple():

    null = tuple('0')
    jobfieldnum = 13
    transfieldnum = 11
    def __init__(self):
        self.database = database.DataBase()
        self.host = self.database.host
        self.port = self.database.port
        self.user = self.database.user
        self.passwd = self.database.passwd
        self.db = self.database.db
        self.begainInsert()
    def begainInsert(self):
        self.conn = pymysql.connect(host = self.host,port =self.port, user = self.user,passwd =self.passwd,
                                    db= self.db)
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    def endInsert(self):

        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
    def insertJobinfo(self,data):
        self.data = data
        if len(self.data) < self.jobfieldnum :
            for i in range(len(self.data),self.jobfieldnum):
                self.data += self.null
        elif len(self.data) > self.jobfieldnum:
            print('字段数过多')
        else :
            pass


        sql = configsql.insert_job_info
        sql = sql.format(self.data)
        print(self.data)
        try:
            self.conn.ping(reconnect=True)
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print('  成功写入')
        except:
            # Rollback in case there is any error
            self.conn.rollback()
            print('执行失败')
            quit()

    def insertTransinfo(self,data):
        self.data = data
        if len(self.data) <self.transfieldnum :
            for i in range(len(self.data),self.transfieldnum):
                self.data+=self.null
        elif len(self.data) > self.transfieldnum:
            print('字段数过多')
        else :
            pass
        sql = configsql.insert_trans_info
        sql = sql.format(self.data)

        try:
            # 执行sql语句
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            #print(str(data)+'  成功写入')
            print(self.data)
            print('  成功写入')
        except:
            # Rollback in case there is any error
            self.conn.rollback()
            print(self.data)
            print('执行失败')
            quit()
        # 关闭光标对象





class Mysql():

    def __init__(self):
        self.info = 0
        self.database = database.DataBase()
        self.host = self.database.host
        self.port = self.database.port
        self.user = self.database.user
        self.passwd = self.database.passwd
        self.db = self.database.db
    def begainConnection(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                    db=self.db)
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()  # 执行完毕返回的结果集默认以元组显示

    def endConnection(self):
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
    # 清空临时表
    def clearTable(self):
        sql = dml.clear_sql
        self.begainConnection()
        try:
            # 执行sql语句
            self.conn.ping(reconnect=True)
            for i in re.findall('.*;', sql):
                print(i)
                self.cursor.execute(i)
            print('  成功写入')
        except:
            # Rollback in case there is any error
            self.conn.rollback()
            print(' 写入失败')


        self.endConnection()
        print('临时表已清空')

    def writeTable(self,sql):
        sql = dml.sql
        self.begainConnection()
        try:
            # 执行sql语句
            self.conn.ping(reconnect=True)
            for i in re.findall('.*;',sql):
                print(i)
                self.cursor.execute(i)
            # self.cursor.execute(sql_3)
            # self.cursor.execute(sql_4)
            print('sql已经执行')
        except:
            # Rollback in case there is any error
            self.conn.rollback()
            print('执行失败')
            quit()
        self.endConnection()

if __name__ == '__main__':
    list  = ('hw', 'ha', '', '', '', '')
    list2 = ('hw', 'ha', '', '', '')
    # 定义要执行的SQL语句

    # insert = MysqlInsertTuple()
    # insert.insertJobinfo(list)
    # insert.insertTransinfo(list2)
    my = Mysql()
   # my.clearTable()
    my.writeTable(dml.sql)
