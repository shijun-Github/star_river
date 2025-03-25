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
from flask import Flask, jsonify, request, Blueprint, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.append('..')  # 假设'..'是drama和utils的父目录
# from rank.drama_recommend_home import *

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


# 创建蓝图实例
blueprint_goods = Blueprint('goods', __name__, url_prefix='/')  # 注意这里的 url_prefix 在 app.py 中会再次被覆盖

# 定义全局变量, 定期更新， 例如将数据库中的内容定期更新到这个变量中就可以了
# 服务每次请求可以直接读取该变量，不需要去数据库中拉，极大提高速度
goods_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/jd_goods_info.csv')

def persist_data_in_service():
    global goods_info # 声明我们要使用全局变量
    goods_info = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/jd_goods_info.csv')
    # print(goods_info)
    print('goods persist_data_in_service', time.time(), 'goods_info.shape:', goods_info.shape)


def start_scheduler():
    """
    定时刷新数据
    redis_es_filter_realtime()
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(persist_data_in_service, 'interval', seconds=1*1*60)
    # scheduler.add_job(loadFaisIndex, 'interval', seconds=60 * 60)
    scheduler.start()


start_scheduler()

@blueprint_goods.route("/goods/home/recommend", methods=["POST", "GET"])
def inter_goods_home_recommend():
    """
    剧主页推荐
    """
    parm_in = json.loads(request.get_data().decode("utf-8"))
    df_deal = goods_info[goods_info['channel'] == parm_in['channel']]
    df_deal_page = df_deal[(parm_in['page_index'] - 1) * parm_in['page_size']: parm_in['page_index'] * parm_in['page_size']]
    # df_deal_page_dict = df_deal_page.to_dict(orient='records')
    # print(df_deal_page_dict)
    # pprint(df_deal_page_dict[0])
    res = []
    for index, row in df_deal_page.iterrows():
        res.append({
            'item_id': row['item_id'],
            'item_name': row['item_name'],
            'author_name': row['author_name'],
            'cover_url': row['cover_url'],
            'extend': json.loads(row['extend'])
        })
    print('哈哈哈哈哈哈哈哈哈： ', len(res) ,res)
    return res



