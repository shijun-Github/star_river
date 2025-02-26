# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint
from turtledemo.forest import symRandom

import pandas as pd
import requests
import json
import time
import random
from backend.utils.product_sign import get_sign_jd_dataoke

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


def func_main_goods_home_recommend_new(parm_in):
    path_data = os.getcwd().split('backend')[0] + 'backend\goods\data\jd_goods_info.csv'
    goods_info = pd.read_csv(path_data)
    goods_info['resourceInfo'] = goods_info.apply(lambda x: json.loads(x['resourceInfo'].replace("'", '"')), axis=1)
    print('goods_info: ', '\n', goods_info)
    print(goods_info['resourceInfo'])
    goods_info.apply(lambda x: print('1111111', type(x['resourceInfo']), x['resourceInfo'], x['resourceInfo']['eliteId']), axis=1)
    print(goods_info['resourceInfo']['eliteId'])
    # df_deal = goods_info[goods_info['resourceInfo']['eliteId'] == parm_in['channel']]
    # df_deal_page = df_deal[(parm_in['page_index'] - 1) * parm_in['page_size']: parm_in['page_index'] * parm_in['page_size']]
    # print('df_deal_page: ', '\n', df_deal_page)
    time.sleep(111)
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


def func_main_goods_home_recommend(parm_in):
    path_data = os.getcwd().split('backend')[0] + 'backend\goods\data\jd_goods_info.csv'
    goods_info = pd.read_csv(path_data)
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

if __name__ == '__main__':
    """
    首页视频推荐
    """
    parm = {
        'page_index': 1,
        'page_size': 10,
        'channel': 1
    }
    t = func_main_goods_home_recommend(parm)
    pprint(t)