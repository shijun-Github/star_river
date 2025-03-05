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
import faiss
import pandas as pd
import requests
import redis
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.append('..')  # 假设'..'是drama和utils的父目录
from aa_recommend_complete_project.rank import drama_recommend_home
from utils.config_constants import get_env_config

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

app = Flask(__name__)


def start_scheduler():
    """
    定时刷新数据
    :return:   redis_es_filter_realtime()
    """
    scheduler = BackgroundScheduler()
    print(123)
    # scheduler.add_job(func_save_drama_info_to_redis, 'interval', seconds=60 * 60)
    # scheduler.add_job(loadFaisIndex, 'interval', seconds=60 * 60)
    scheduler.start()


@app.route("/short_drama/home/recommend", methods=["POST", "GET"])
def inter_short_drama_home_recommend():
    """
    短剧主页推荐
    """
    if request.method == 'GET':
        parameters = request.args.to_dict()
    else:
        parameters = json.loads(request.get_data().decode("utf-8"))
    parm = {
        'env': 'uat',
        'user_id': '11111',
        'page_index': 1,
        'page_size': 10,
    }
    re_data = drama_recommend_home.func_main_run(parm)
    res = {
        "return_code": 0,
        "return_message": "success",
        "data": re_data
    }
    return res



if __name__ == '__main__':
    """
    服务
    gunicorn -w 4 -b 0.0.0.0:8528 start_service.py:app
    """
    print("扛起大刀。。。")
    env_ = 'uat'  # sys.argv[1]
    config = get_env_config(env_)
    port_dict = {'test': 8588, 'uat': 8589, 'prod': 8590}
    thread_dict = {'test': 1, 'uat': 1, 'prod': 1}
    redis_client = redis.StrictRedis(host=config['redis']['1']['host'], port=config['redis']['1']['port'],
                                     password=config['redis']['1']['password'])

    # start_scheduler()  # 定期更新基础数据
    app.run(host='0.0.0.0', port=port_dict[env_], debug=False)
    # serve(app, host='0.0.0.0', port=port_dict[env_], threads=thread_dict[env_])

