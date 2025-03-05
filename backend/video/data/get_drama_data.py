import json
import re
import sys
import time
from pprint import pprint

import numpy as np
import pandas as pd
import pymysql
import os
import webbrowser
import math
import faiss
import requests
import jieba
from gensim.models import word2vec, Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils import shuffle

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

sys.path.append('../..')  # 假设'..'是drama和utils的父目录
from utils.func_mysql import get_data_from_mysql
from utils.config_constants import get_env_config


def  func_get_drama(config):
    """
     t_star_blog： release_source = 32 and publish_scene = 66  表示短剧
     t_star_blog_drama  ： drama_type ：短剧类型：0-短剧 2-合集 3-影视剧 10-电影
     t_star_blog_drama_video_relation
    """
    # 获取剧级别的信息
    drama_info = get_data_from_mysql(sql_input="""(
                        select id as drama_id, drama_type, video_num, last_num_position, drama_cover_url
                            ,drama_name, drama_desc
                        from hobby_star_blog.t_star_blog_drama
                        where deleted=0 and drama_type in (0, 3, 10)
                        )""", config=config, mysql_config='1')
    pprint(drama_info.to_dict(orient='records'))
    print(drama_info)
    print(drama_info.groupby('drama_type').size())

    # 获取分级信息
    video_info = get_data_from_mysql(sql_input="""(
                        select t2.id as video_id, t2.episode
                        , t2.drama_id, t1.drama_name, t1.drama_type
                        # , t2.introduction , t3.content_desc
                        , t3.cover_url as video_cover_url, t3.video_url
                        from hobby_star_blog.t_star_blog_drama t1
                        join hobby_star_blog.t_star_blog_drama_video_relation t2 on t1.id=t2.drama_id
                        join hobby_star_blog.t_star_blog t3 on t2.business_id = t3.id
                        where t1.drama_type in (0, 3, 10) and  t2.deleted=0 and t3.deleted=0 
                        )""", config=config, mysql_config='1')
    pprint(video_info.head(20).to_dict(orient='records'))
    print(video_info)

    # # 获取当前脚本文件的绝对路径
    # current_file_path = os.path.abspath(__file__)
    # # 获取当前脚本文件所在的目录
    # current_directory = os.path.dirname(current_file_path)
    # print(current_file_path)
    # print(current_directory)

    drama_info.to_csv('drama_info.csv', index=False)
    video_info.to_csv('video_info.csv', index=False)


if __name__ == '__main__':
    """ 主要是获取视频的信息，视频分成两级
     drama 剧集级别，第一层     短剧   剧集    电影
     video 单集级别，第二层    具体集  具体集   电影"""
    config = get_env_config('prod')
    func_get_drama(config=config)
