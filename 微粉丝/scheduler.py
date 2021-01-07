"""
@Time ： 2020/10/29 10:06 上午
@Auth ： FY
@File ：scheduler.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from spider import *
import sys


executers = {
    "default": ThreadPoolExecutor(2)
}


def run1(ip, port, username, password, database, table_name):
    scheduler = BlockingScheduler(executers=executers)
    scheduler.add_job(main, 'interval', minutes=5,
                      kwargs={"ip": ip, "port": port, "username": username, "password": password, "database": database,
                              "table_name": table_name})
    scheduler.start()


params = sys.argv[1:]

if __name__ == '__main__':
    run1(*params)

    # 运行代码时：python scheduler.py ip port username password database table_name
