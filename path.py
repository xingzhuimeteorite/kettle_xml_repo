# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import re

class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """
    #设置三级目录字典
    job_dic = {}
    job_count = 0
    trans_count = 0
    other_count = 0

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
        elif self.pathname.is_dir():
            self.tree += '    |' * n + '-' * 4 + \
                         str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)

    def set_job_dic(self,n=0):
        if self.pathname.is_file():
            if re.search('.kjb',self.pathname.name) != None:
                self.job_count=self.job_count+1
            elif re.search('.ktr',self.pathname.name) != None:
                self.trans_count = self.trans_count + 1
            else:
                self.other_count = self.other_count + 1
        elif self.pathname.is_dir():
            if n==2 :
                self.job_dic[str(self.pathname.relative_to(self.pathname.parent)) ] = self.pathname.parent.name+'/'+self.pathname.name
            else :
                pass
            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.set_job_dic(n + 1)

    def count(self):
        self.set_job_dic()
        print("job任务数  "+str(len(self.job_dic)))
        print("job_文件数  "+str(self.job_count))
        print("trans_文件数  "+str(self.trans_count))
        print("其他文件数  "+str(self.other_count))


dirtree = DirectionTree()
dirtree.set_path('E:\work\etl\jordan\Penuel\kettle_repo')
# dirtree.generate_tree()
# print(dirtree.tree)
dirtree.set_job_dic()
print(dirtree.job_dic)
dirtree.count()

