# -*- coding: utf-8 -*-
import json
import math
import os
import time
import sys
from datetime import datetime, timedelta
from pprint import pprint
from threading import Thread, Lock
from waitress import serve
import pandas as pd
import requests
from flask import Flask, jsonify, request
# from OpenSSL import SSL
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.append('..')  # 假设'..'是drama和utils的父目录

from backend.goods.goods_inter import blueprint_goods
from backend.video.video_inter import blueprint_video

# from rank.drama_recommend_home import *
# from video.recall import base_rec, keyword_search, search_func
pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(blueprint_video, url_prefix='/')
app.register_blueprint(blueprint_goods, url_prefix='/')


if __name__ == '__main__':
    """
    服务
        gunicorn -w 4 -b 0.0.0.0:8528 video_service.py:app
        nohup python video_service.py
    该程序 已启动本地服务 ps -ef|grep video_service.py
    (37)  start python .\video_service.py
    pip -i https://pypi.tuna.tsinghua.edu.cn/simple install scikit-learn
    """
    print("扛起大刀。。。")
    app.run(host="0.0.0.0", port=8588, debug=False)
    # serve(app, host='0.0.0.0', port=8588, threads=3)


