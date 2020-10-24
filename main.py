#!C:\Users\gsyang\AppData\Local\Programs\Python\Python36 python36

# -*- encoding: utf-8 -*-

'''
@Author  :   xingzhui

@License :   (C) Copyright 2020-2020, 乐其

@Contact :   gsyang@leqee.com

@Software:   解析kettle资源库

@File    :   main.py

@Time    :   2020/09/09

@Desc    :  xml文件解析

'''


from pathlib import Path
import re
import job
import transform
import mysql
import config.dmlpro as dml


def get_path(pathname):
    '''
    获取当前资源库下 相对目录
    :param pathname: Path下子元素 可迭代寻找父元素
    :return:
    '''
    if pathname.parent.parent.name == 'kettle_repo':
        return '/'+str(pathname.parent.name)
    else :
        return '/'+str(pathname.parent.parent.name)+'/'+str(pathname.parent.name)

def findall_repo(pathname, n=0):
    '''
    递归文件夹
    :param pathname:  pathlib对象
    :param n:   文件夹递归层数
    :return:
    '''

    if pathname.is_file():
       #  .kjb文件生成job对象
       if re.search('.kjb',pathname.name) != None:
           print('解析----'+str(pathname.name))
           thisjob = job.Job(str(pathname),get_path(pathname),str(pathname.name),pathname.parent)
           thisjob.setEntries()
           del thisjob
       #   .ktr文件生成trans对象
       elif re.search('.ktr', pathname.name) != None:
           print('解析----' + str(pathname.name))
           thistrans = transform.Transform(str(pathname),get_path(pathname),str(pathname.name),pathname.parent)
           thistrans.setSteps()
           del thistrans
       else:
           # 其他文件 不参与解析
           print('跳过----' + str(pathname.name))
    elif pathname.is_dir():
        #文件夹进行 递归迭代
        for cp in pathname.iterdir():
            findall_repo(cp, n + 1)


if __name__ == '__main__':

    # 连接数据库
    my = mysql.Mysql()
    # 清空写入表
    my.clearTable()
    # 遍历资源库目录 插入解析数据
    path = Path(r'E:\work\etl\jordan\Penuel\kettle_repo')
    findall_repo(path)
    #生成最终表
    my.writeTable(dml.sql)

'''
windows python 3.6
工位网络
本机下资源库目录
09-03
预计用时九 ~ 十三分钟
09-04
12.06 - 1213
16.37 - 16.42
七分钟
'''