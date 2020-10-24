# windows python 3.8

import xml.etree.ElementTree as ET
import mysql

def insert(data):
    insert = mysql.MysqlInsertTupleJob()
    insert.insert(data)
class Sql_script():

    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = step.find("connection").text
        self.sql = step.find("sql").text
        self.parentname = parentname
    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        print(self.connection)
        print(self.sql)
        print(self.parentname)

    def getInfo(self):
        data = (self.parentname,self.name,self.type,self.connection,self.sql)
        return data
class Trans():

    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        #self.directory = step.find("directory").text
        self.transname = step.find("transname").text
        self.parentname = parentname

    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        #print(self.directory)
        print(self.transname)
        print(self.parentname)

    def getInfo(self):
        data = (self.parentname,self.name,self.type,'','')
        return data
class Empty():

    def __init__(self, step,parentname):
        self.parentname = parentname

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.parentname,'','','','请定义')
        return data
class Job():
    # 定义实体字典
    entries = {}

    # 定义连接字典
    hops = {}

    # 定义组件字典
    entities = {}

    # 构造函数
    def __init__(self,jobname,parentname):
        __tree = ET.parse(jobname)
        self.root = __tree.getroot()
        self.jobname = jobname
        self.name = self.root.find("name").text
        self.directory = self.root.find("directory").text
        self.created_date = self.root.find("created_date").text
        self.modified_date = self.root.find("modified_date").text
        self.parentname = parentname
        self.job_info = (self.name,self.directory,self.created_date,self.modified_date)
    def selfIntroduction(self):
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
                self.entities[name] = Sql_script(entry,self.parentname)
                #self.entities[name].selfIntroduction()

            elif type == 'TRANS':
                self.entities[name] = Trans(entry,self.parentname)
                #self.entities[name].selfIntroduction()

            else:
                self.entities[name] = Empty(entry,self.parentname)
                #self.entities[name].selfIntroduction()
            entry_info  = self.entities[name].getInfo()
            data = self.job_info+entry_info
            insert(data)

    def setHops(self):
        hops = self.root.find("hops")
        for hop in hops.findall("hop"):
            hop_from = hop.find("from").text
            hop_to = hop.find("to").text
            self.hops[hop_from] = hop_to

if __name__ == '__main__':
    job = Job(r"E:\work\etl\jordan\Penuel\kettle_repo\arnon\arnon_2copt_shop_cat_month\Job_arnon_2copt_shop_cat_month.kjb",'root')
    job.selfIntroduction()
    job.setEntries()
    # job.setHops()
    # # print(job.entries)
    # for k in job.entities.keys():
    #     print(k)
    #     job.entities[k].selfIntroduction()