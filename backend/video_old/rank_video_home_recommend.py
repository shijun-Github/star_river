# -*- coding: utf-8 -*-
import json
import os
import sys
from pprint import pprint
import pandas as pd
from backend.utils import func_mysql
from sklearn.utils import shuffle

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


def func_main_video_home_recommend(input_parameter):
    df_deal = func_mysql.func_get_data_from_mysql("select * from video.video_baidu_haokan")
    res = []
    if df_deal.shape[0] > 0:
        df_deal = df_deal[(input_parameter['page_index'] - 1) * input_parameter['page_size']: input_parameter['page_index'] * input_parameter['page_size']]
        df_deal = df_deal.sort_values('publish_time', ascending=False)
        df_deal = shuffle(df_deal)
        for index, row in df_deal.iterrows():
            res.append({
                'item_id': row['id'],
                'item_name': row['title'],
                'author_name': row['source_name'],
                'cover_url': row['poster_small'],
                'extend': {
                    'url': row['play_url'],
                    'duration': row['duration']
                }
            })
    return res

if __name__ == '__main__':
    """
    首页视频推荐
    """
    parm = {
        'page_index': 1,
        'page_size': 10,
        'channel': 'yunying_vlog'
    }
    t = func_main_video_home_recommend(parm)
    pprint(t)