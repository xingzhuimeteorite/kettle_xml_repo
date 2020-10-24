#!C:\Users\gsyang\AppData\Local\Programs\Python\Python36 python36

# -*- encoding: utf-8 -*-

'''
@Author  :   xingzhui

@License :   (C) Copyright 2020-2020, 乐其

@Contact :   gsyang@leqee.com

@Software:   kettle.kjb文件对象解析

@File    :   job.py

@Time    :   2020/09/09

@Desc    :  xml文件解析

'''

import xml.etree.ElementTree as ET
import mysql
import sqlanalysis
import re
import gitinfo

# 生成测试数据库连接对象
insert_job = mysql.MysqlInsertTuple()

def insert(data):
    '''
    数据库插入
    :param data: 元组对象 demo:('job_demo.kjb','/demo/demo1','job_demo','/demo/demo','2020-09-09 09:09:09','2020-09-09 16:51:37', '小明','Start', 'SPECIAL', '', '开始', 0, '0')
    :return:
    '''
    global  insert_job
    # 数据插入
    insert_job.insertJobinfo(data)
    #del insert
class Empty():
    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.parentname = parentname

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name ,self.type,'','有新类型，请修改代码进行解析')
        return data
class JobInfo():
    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.jobname = step.find("jobname").text
        self.directory = step.find("directory").text
        self.parentname = parentname

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,self.directory,self.jobname)
        return data

class Simple_eval():

    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.parentname = parentname

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class TableContent():
    def __init__(self, step, parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = step.find("connection").text
        self.tablename = str(step.find("tablename").text)
        self.parentname = parentname

    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        print(self.connection)
        print(self.tablename)
        print(self.parentname)
        print(self.getInfo())

    def getInfo(self):
        data = ( self.name, self.type, self.connection, self.tablename)
        return data
class Begin():
    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text

        self.parentname = parentname
    def selfIntroduction(self):
        print(self.name)
        print(self.type)

        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','开始')
        return data

class Success():
    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text

        self.parentname = parentname
    def selfIntroduction(self):
        print(self.name)
        print(self.type)

        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','成功')
        return data



class Sql_script():
    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = step.find("connection").text
        self.sql = step.find("sql").text
        self.parentname = parentname
        self.maxcomplexity = sqlanalysis.SqlAnalysis(self.sql).getMaxComplexity()
        self.size = sqlanalysis.SqlAnalysis(self.sql).getSqlSize()
    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        print(self.connection)
        print(self.sql)
        print(self.parentname)

    def getInfo(self):
        data = (self.name,self.type,self.connection,self.sql,self.maxcomplexity,self.size)
        return data
class Trans():

    def __init__(self, step,parentname):
        self.step = step
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.transname = step.find("transname").text
        self.directory = self.check_info()
        self.parentname = parentname

    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        print(self.directory)
        print(self.transname)
        print(self.parentname)

    def getInfo(self):
        data = (self.name,self.type,self.directory,self.transname)
        #print(data)
        return data
    def check_info(self):
        if  self.step.find("directory") == None:
            print(str(self.step.find("filename").text))
            print(re.findall('/\w*',self.step.find("filename").text)[-1].lstrip('/'))
            self.transname = re.findall('/\w*',self.step.find("filename").text)[-1].lstrip('/')

            return str(re.findall('/\w*', self.step.find("filename").text)[0] + re.findall('/\w*', self.step.find("filename").text)[1])
        if  self.step.find("directory").text == '/':
            return '${Internal.Entry.Current.Directory}'
        else :
            return self.step.find("directory").text

class Job():
    # 定义实体字典
    entries = {}

    # 定义连接字典
    hops = {}

    # 定义组件字典
    entities = {}

    # 构造函数
    def __init__(self,job_file_name,file_pathname,filename,path):
        __tree = ET.parse(job_file_name)
        self.root = __tree.getroot()
        self.filename = str(filename).replace('.kjb','')
        self.file_pathname = file_pathname
        self.name = self.root.find("name").text
        self.directory = self.root.find("directory").text
        self.created_date = self.root.find("created_date").text
        self.modified_date = self.root.find("modified_date").text
        self.author = gitinfo.gitInfo().getAutorInfo(path,filename)
        self.job_info = self.getInfo()

    def selfIntroduction(self):
        print(self.filename)
        print(self.file_pathname)
        print(self.name)
        print(self.directory)
        print(self.created_date)
        print(self.modified_date)

    def getEntries(self):
        entries = self.root.find("entries")
        for entry in entries.findall("entry"):
            name = entry.find("name").text
            type = entry.find("type").text
            self.steps[name] = type
            print(name, type)

    def setEntries(self):
        entries = self.root.find("entries")
        for entry in entries.findall("entry"):
            name = entry.find("name").text
            type = entry.find("type").text
            self.entries[name] = type
            if type == 'SQL':
                self.entities[name] = Sql_script(entry,self.name)
                #self.entities[name].selfIntroduction()
            elif type == 'JOB':
                self.entities[name] = JobInfo(entry,self.name)
                #self.entities[name].selfIntroduction()
            elif type == 'TRANS':
                self.entities[name] = Trans(entry,self.name)
                #self.entities[name].selfIntroduction()
            elif type == 'SPECIAL':
                self.entities[name] = Begin(entry,self.name)
            elif type == 'SIMPLE_EVAL':
                self.entities[name] = Simple_eval(entry,self.name)
            elif type == 'EVAL_TABLE_CONTENT':
                self.entities[name] = TableContent(entry,self.name)

            elif type == 'SUCCESS':
                self.entities[name] = Success(entry,self.name)
            else:
                self.entities[name] = Empty(entry,self.name)
                #self.entities[name].selfIntroduction()
            entry_info  = self.entities[name].getInfo()
            data = self.job_info+entry_info
            insert(data)
    def getInfo(self):
        data = (self.filename, self.file_pathname, self.name, self.directory,self.created_date,self.modified_date,self.author)
        return data

    def setHops(self):
        hops = self.root.find("hops")
        for hop in hops.findall("hop"):
            hop_from = hop.find("from").text
            hop_to = hop.find("to").text
            self.hops[hop_from] = hop_to

if __name__ == '__main__':
    job = Job(r"E:\work\etl\jordan\Penuel\kettle_repo\tiberias\tiberias_2copt_shop_lowprice_related_index_daily\temp.kjb",'root','root')
    job.selfIntroduction()
    #job.setEntries()
    #job.setHops()
    print(job.entries)
    for k in job.entities.keys():
        print(k)
        job.entities[k].selfIntroduction()