# -*- coding: utf-8 -*-

import os
import re
import subprocess

ruler = '(?<=Author: ).*(?= <)'
# ruler = '(?<=Author: ).*>'
author_map = {
'jlwang5':'汪金亮'
,'yhgu':'顾银河'
,'gyihen':'顾银河'
,'yxyang1':'杨云霞'
,'kpwang':'王克鹏'
,'jguo1':'郭健'
,'ljlou@leqee.com':'娄玲娟'
,'ddhan1':'韩丹丹'
,'unknown':'杨国胜'
,'yfzhu3':'朱育锋'
,'shzheng':'郑思海'
,'hfeng1':'冯华'
,'jqdai':'戴杰泉'
,'mxhan':'韩旻翔'

}

class gitInfo():
    def __init__(self):
        pass
    def getAutorInfo(self,path,filename):
        try:
            os.chdir(path)
            out, err = subprocess.Popen('git log ' + str(filename),stdout=subprocess.PIPE).communicate()
            txt = out.decode('utf-8')
            autorinfo = re.findall(ruler, txt)[0]
            # print(autorinfo)
            if (autorinfo in author_map):
                return author_map[autorinfo]
            else:
                return autorinfo
        except:
            print('命令行系统错误')
            return 'error'

if __name__ == '__main__':
    path  =  r'E:\work\etl\jordan\Penuel\kettle_repo\tiberias\tiberias_2bopt_goods_xls_lst_product_analyse_new'
    filename = 'Job_tiberias_2bopt_goods_xls_lst_product_analyse_new.kjb'
    out = gitInfo().getAutorInfo(path,filename)
    print(out)
