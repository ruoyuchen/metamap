# !/usr/bin/env python
# -*- coding: utf-8 -*
'''
created by will
'''

import multiprocessing, os

print('gunicorn config is running....')

bind = "0.0.0.0:8088"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = '/tmp/gunicorn.pid'
# accesslog = '/tmp/gunicorn_access.log'
errorlog = '/tmp/gunicorn_error.log'
loglevel = 'info'
capture_output = True
# statsd_host = 'localhost:8077'
proc_name = 'will\'s metamap'
daemon = True
# 测试确定，这里设置这个参数不生效
# django_settings = 'metamap.config.prod'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metamap.config.prod")
