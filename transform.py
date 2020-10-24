# windows python 3.8

import xml.etree.ElementTree as ET
import mysql
import sqlanalysis
import gitinfo

insert_trans = mysql.MysqlInsertTuple()
def insert(data):
    global insert_trans
    insert_trans.insertTransinfo(data)
    #del insert
class Empty():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','有新类型，请修改代码进行解析')
        return data

class SelectValues():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class PrioritizeStreams():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class GetVariable():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class SetVariable():

    def __init__(self, step, parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)

    def getInfo(self):
        data = (self.name, self.type, '', '')
        return data


class RowsToResult():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class RowsFromResult():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text

    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,'','')
        return data

class SqlScript():

    def __init__(self, step,parentname):
        self.parentname = parentname
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = self.checkInfo(step.find("connection").text)
        self.sql = self.checkInfo(step.find("sql").text)
        self.maxcomplexity = sqlanalysis.SqlAnalysis(self.sql).getMaxComplexity()
        self.size = sqlanalysis.SqlAnalysis(self.sql).getSqlSize()


    def selfIntroduction(self):
        print('未定义')
        print(self.parentname)
        print(self.getInfo())

    def getInfo(self):
        data = (self.name,self.type,self.connection,self.sql,self.maxcomplexity,self.size)
        #print(data)
        return data

    def checkInfo(self,value):
        if value == None :
            return ''
        else :
            return value

class TableInput():

    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = self.checkInfo(step.find("connection").text)
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

    def checkInfo(self, value):
        if value == None:
            return ''
        else:
            return value

class TableOutput():

    def __init__(self, step,parentname):
        self.name = step.find("name").text
        self.type = step.find("type").text
        self.connection = step.find("connection").text
        self.table = step.find("table").text
        self.parentname = parentname
    def selfIntroduction(self):
        print(self.name)
        print(self.type)
        print(self.connection)
        print(self.table)
        print(self.parentname)
    def getInfo(self):
        data = (self.name,self.type,self.connection,self.table)
        return data

class Transform():
    # 定义实体字典
    steps = {}

    # 定义连接字典
    hops = {}

    # 定义组件字典
    entities = {}

    def __init__(self,transform_file_name,file_pathname,filename,path):
        __tree = ET.parse(transform_file_name)
        self.root = __tree.getroot()
        self.filename = str(filename).replace('.ktr', '')
        self.file_pathname = file_pathname
        self.name = self.root.find("info").find("name").text
        self.directory = self.checkInfo(self.root.find("info").find("directory").text)
        self.author = gitinfo.gitInfo().getAutorInfo(path,filename)
        self.transinfo = self.getInfo()
    def getInfo(self):
        data = (self.filename,self.file_pathname,self.name,self.directory,self.author)
        return data
    def selfIntroduction(self):
        print(self.name)
        print(self.directory)
    def checkInfo(self,value):
        if value == '/' :
            return self.file_pathname
        else :
            return value
    def setSteps(self):
        for step in self.root.findall("step"):
            name = step.find("name").text
            type = step.find("type").text
            entity = step
            self.steps[name] = type
            if type == 'TableInput':
                self.entities[name] = TableInput(step,self.name)
            elif type == 'TableOutput':
                self.entities[name] = TableOutput(step,self.name)
            elif type == 'ExecSQL':
                self.entities[name] = SqlScript(step,self.name)
            elif type == 'RowsFromResult':
                self.entities[name] = RowsToResult(step,self.name)
            elif type == 'RowsToResult':
                self.entities[name] = RowsToResult(step,self.name)
            elif type == 'SetVariable':
                self.entities[name] = SetVariable(step,self.name)
            elif type == 'SelectValues':
                self.entities[name] = SelectValues(step,self.name)
            elif type == 'GetVariable':
                self.entities[name] = GetVariable(step,self.name)
            elif type == 'PrioritizeStreams':
                self.entities[name] = PrioritizeStreams(step,self.name)

            else:
                self.entities[name] = Empty(step,self.name)

            step_info = self.entities[name].getInfo()
            data = self.transinfo + step_info
            insert(data)

            # self.entities[name].selfIntroduction()

    def setHops(self):
        hops = self.root.find("order")
        for hop in hops.findall("hop"):
            hop_from = hop.find("from").text
            hop_to = hop.find("to").text
            self.hops[hop_from] = hop_to


if __name__ == '__main__':
    trans = Transform(r"E:\work\etl\jordan\Penuel\kettle_repo\arnon\arnon_2copt_shop_whole_quota_sycm_daily_v1_extend\Trans_arnon_2copt_sycm_crm_member_sale_daily_ind_mtd_tot.ktr",'root','Trans_arnon_2copt_sycm_crm_member_sale_daily_ind_mtd_tot.ktr')
    trans.selfIntroduction()
    trans.setSteps()
