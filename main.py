#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2023/2/14 9:37
# @Author       : Tridro
# @Email        : tridro@beneorigin.com
# @Project      : chatgpt-on-wxwork
# @File         : main.py
# @Software     : PyCharm
# All Copyright Reserved

import setproctitle

import app

setproctitle.setproctitle("chatgpt-on-wxwork")


if __name__ == '__main__':
    app.start_fastapi()
