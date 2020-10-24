from pathlib import Path
import re
import job
# import transform


def findall_repo(pathname, n=0):

    if pathname.is_file():
       if re.search('.kjb',pathname.name) != None:
           print('解析----'+str(pathname.name))
           thisjob = job.Job(str(pathname),str(pathname.parent.name))
           thisjob.setEntries()
       elif re.search('.ktr', pathname.name) != None:
           print('解析----' + str(pathname.name))
       else:
           print('跳过----' + str(pathname.name))
    elif pathname.is_dir():
        for cp in pathname.iterdir():
            findall_repo(cp, n + 1)


if __name__ == '__main__':
    path = Path('E:\work\etl\jordan\Penuel\kettle_repo')
    findall_repo(path)
