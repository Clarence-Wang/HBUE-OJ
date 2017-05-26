# coding:utf-8

import os

# 降低程序运行权限，防止恶意代码
import threading
from Queue import Queue

import logging

import time

from judge import config


def low_level():
    try:
        os.setuid(int(os.popen("id -u %s" % "nobody").read()))
    except:
        pass


q = Queue(config.queue_size)
dblock = threading.Lock()


def start_work_thread():
    """开启工作线程"""
    for i in range(config.count_thread):
        from judge.worker import get_task_from_queue
        t = threading.Thread(target=get_task_from_queue)
        t.deamon = True
        t.start()


def start_get_task():
    """开启获取任务线程"""
    from judge.producer import put_task_into_queue
    t = threading.Thread(target=put_task_into_queue, name="get_task")
    t.deamon = True
    t.start()


def check_thread():
    low_level()
    '检测评测程序是否存在,小于config规定数目则启动新的'
    while True:
        try:
            if threading.active_count() < config.count_thread + 2:
                logging.info("start new thread")
                from judge.worker import get_task_from_queue
                t = threading.Thread(target=get_task_from_queue)
                t.deamon = True
                t.start()
            time.sleep(1)
        except:
            pass


def start_protect():
    """开启守护进程"""
    low_level()
    t = threading.Thread(target=check_thread, name="check_thread")
    t.deamon = True
    t.start()


def main():
    low_level()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s --- %(message)s', )
    start_get_task()
    start_work_thread()
    start_protect()


if __name__ == '__main__':
    main()
