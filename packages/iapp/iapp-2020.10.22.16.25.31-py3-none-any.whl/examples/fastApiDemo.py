#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : fastApiDemo
# @Time         : 2020/10/22 4:22 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from iapp import App


app = App()

func = lambda **kwargs: kwargs

app.add_route("/demo", func)
# app.run(port=1234)

app.run(app.app_file_name(__file__), port=1234)