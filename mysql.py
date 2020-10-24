import pymysql

class MysqlInsertTupleJob():

    def __init__(self):
        # 连接database
        self.conn = pymysql.connect("bi-test-polardb.rwlb.rds.aliyuncs.com","office_test","pz1ytq1WCT2Z2bNR","dev_hermon" )
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
        #cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    def insert(self,data):
        sql = """
            INSERT INTO `dev_hermon`.`job_info`
            (  `job_name`
            , `job_path`
            , `job_create_time`
            , `job_update_time`
            ,`parent_job_name`
            , `job_entry`
            , `job_entry_type`
            , `job_entry_connection`
            , `job_entry_content`
            )
             values {};
            """
        sql = sql.format(data)

        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            #print(str(data)+'  成功写入')
            print('  成功写入')
        except:
            # Rollback in case there is any error
            self.conn.rollback()
            print('执行失败')
        # 关闭光标对象

        self.cursor.close()

        # 关闭数据库连接
        self.conn.close()

if __name__ == '__main__':
    list  = ( 'hw', 'ha', 'hr', '', '', '1', '1', '1', '1')
    # 定义要执行的SQL语句

    insert = MysqlInsertTupleJob()
    insert.insert(list)



