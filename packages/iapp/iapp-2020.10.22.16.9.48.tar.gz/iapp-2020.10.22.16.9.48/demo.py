#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : demo
# @Time         : 2019-12-10 20:05
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import logging

from loguru import logger

from sanic import Sanic
from sanic.response import json


logging.getLogger("sanic.root").handlers.clear()
trace = logger.add('./runtime_{time}.log',
                   rotation="100 MB",
                   retention='3 days',
                   encoding="utf-8",
                   backtrace=True,
                   diagnose=True)
from sanic import log
# logger = logging.getLogger("sanic.root")
# error_logger = logging.getLogger("sanic.error")
# access_logger = logging.getLogger("sanic.access")
log.logger = logger

# Redirect all logging to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

# logger.remove()
logging.basicConfig(handlers=[InterceptHandler()], level=0)

app = Sanic()





@app.route('/')
async def test(request):
    return json({'hello': 'world'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
