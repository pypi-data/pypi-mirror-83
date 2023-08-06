#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : example
# @Time         : 2019-08-08 14:30
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import sys
import time
import logging
import jieba
from iapp import App
from iapp.scheduler import Scheduler

# PC

d = 2

def task():
    global d
    d = d - 1
    print(d, 1 / d)

    logging.warning(time.ctime())

    global dt
    dt = time.ctime()
    return dt


scheduler = Scheduler()
scheduler.add_job(task, seconds=10)
scheduler.start()

dt = task()
# Api
update = lambda **kwargs: dt
pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
pred2 = lambda x=1, y=1: x - y
pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)

app = App()
app.add_route("/", update, version="1")
app.add_route("/", update, methods="POST")

app.add_route("/f1", pred1, version="1")
app.add_route("/f2", pred2, version="2")
if __name__ == '__main__':
    app.run(debug=True, port=8899)
