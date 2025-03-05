import json
import re
import sys
import time
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
pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

sys.path.append('..')  # 假设'..'是drama和utils的父目录
from utils.func_mysql import get_data_from_mysql
from utils.config_constants import get_env_config




theatre_info =  {
    'item_id': 'id（二级id, 如果是探剧则是剧集id,如果是探瓜则是瓜id, 如果是平行世界则是平行世界的id',
    'source': '来源：0-短剧 1-后台创建 3-影视剧 4-话题剧场 5-实时探瓜',
    'source_id': '一级id, 对应来源的id, 如果是探剧则是剧id, 如果是探瓜则是话题id, 如果是平行世界则是剧id',
    'theatre_id': '剧场id',
    'extend': {
        'name': '一级 名称（vec、key_word、tag     如果是探剧则是剧name, 如果是探瓜则是话题name, 如果是平行世界则是剧name',
        'desc': '一级 描述（vec、key_word、tag',
        'cover_url': '一级 封面链接。（vec,key_word）',
    },
    'name': '名称（vec、key_word、tag',
    'desc': '描述（vec、key_word、tag',
    'cover_url': '封面链接。（vec,key_word）',

    'expose_num_1' :'近1天曝光',
    'click_num_1': '近1天点击',
    'duration_1': '近1天消费时长（秒）',
    'click_rate_1': '近1天点击率（click_num_1/expose_num_1）',
    'duration_rate_1': '近1天曝光时长(duration_1/expose_num_1)',

    'expose_num': '总曝光',
    'click_num': '总点击',
    'duration': '总消费时长',
    'click_rate': '点击率（click_num/expose_num）',
    'duration_rate': '单次曝光时长 (duration_1/expose_num_1)',
}


# 队列是 左进右出, 下面的id是物品表内的item_id
user_info = {
    'user_id': '用户id',
    'gender': '用户性别',
    'age': '年龄',

    'expose_id_list': '曝光的id id,source;id,source;id,source',
    'click_id_list': '点击的id， id,source;id,source;id,source',
    'one_duration_id_list': '消费的时间 id,source,play_time;id,source,play_time;id,source,play_time',
    'agg_duration_id_list': '累计消费的时间 id,source,play_time;id,source,play_time;id,source,play_time',
}


"""
场景： 探剧   平行世界    探瓜    
一级：  剧      剧      话题
二级： 剧集    剧集       瓜

"""




def func_get_drama_video():
    """
    主要是获取短剧类的单个小视频

    """
    # t_star_blog = get_data_from_mysql(sql_input="""(
    #                     select *
    #                     from hobby_star_blog.t_star_blog
    #                     where deleted=0 and type in ('1023')
    #                     limit 1000
    #                 )""", config=config,mysql_config='1')
    # print(t_star_blog)
    # print(t_star_blog[['id', 'cover_url', 'video_url', 'video_duration']])
    #
    # print(t_star_blog[['id', 'cover_url', 'video_url', 'video_duration']].head(3).to_dict(orient='records'))
    #
    # drama_info = get_data_from_mysql(sql_input="""(
    #                     select id as drama_id, drama_name, drama_cover_url, drama_desc, drama_tags, talent_name, category_name, video_num, last_num_position
    #                     from hobby_star_blog.t_star_blog_drama
    #                     where deleted=0
    #                     )""", config=config, mysql_config='1')
    # print(drama_info[['drama_cover_url', 'drama_name']].head(30).to_dict(orient='records'))
    #
    # video_info = get_data_from_mysql(sql_input="""(
    #                     select t2.id as video_id, t2.drama_id, t2.episode, t2.introduction,
    #                         t1.cover_url, t1.video_url
    #                     from hobby_star_blog.t_star_blog t1
    #                     join hobby_star_blog.t_star_blog_drama_video_relation t2 on t1.id=t2.business_id
    #                     where t1.deleted=0 and t2.deleted=0
    #                     )""", config=config, mysql_config='1')
    # print(drama_info)
    # print(video_info.sort_values('drama_id'))
    # print(video_info[['cover_url', 'video_url']].head(30).to_dict(orient='records'))

    # #    , theatre_cover_url, theatre_intro, theatre_name, theatre_prompt
    theatre_info = get_data_from_mysql(sql_input="""(
                        select id as theatre_id, theatre_name, video_num, theatre_intro, theatre_cover_url, source
                        from hobby_star_blog.t_theatre
                        where deleted=0 and status=1 and task_status=10
                        )""", config=config, mysql_config='1')
    print(theatre_info.head(3))

    video_info = get_data_from_mysql(sql_input="""(
                        select t1.id as video_id, t1.cover_url, t1.video_url, t1.video_duration,
                            t2.theatre_id, t2.episode, t2.intro
                        from hobby_star_blog.t_star_blog t1
                        join hobby_star_blog.t_theatre_episode t2 on t1.id=t2.star_blog_id
                        where t1.deleted=0 and t2.deleted=0 and t2.status=1
                        )""", config=config, mysql_config='1')
    print(video_info.head(3))

    theatre_info.to_csv('data/theatre_info.csv', index=False)
    video_info.to_csv('data/video_info.csv', index=False)

    # print(video_info.head(3).to_dict(orient='records'))
    # theatre_video_info = pd.merge(theatre_info, video_info, on='theatre_id')
    # print(theatre_video_info)

def func_get_theatre_video():
    """

    """
    t_star_blog = get_data_from_mysql(sql_input="""(
                        select *
                        from hobby_star_blog.t_star_blog
                        where deleted=0 and type in ('1023')
                        limit 1000
                    )""", config=config,mysql_config='1')
    print(t_star_blog)
    print(t_star_blog[['id', 'content_desc', 'video_duration', 'cover_url', 'video_url']])
    print();    print();print()

    theatre_info = get_data_from_mysql(sql_input="""(
                        select id as theatre_id, theatre_name, video_num, theatre_intro, theatre_cover_url, source
                        from hobby_star_blog.t_theatre
                        where deleted=0 and status=1 and task_status=10
                        )""", config=config, mysql_config='1')

    print(theatre_info.head(10))
    video_info = get_data_from_mysql(sql_input="""(
                        select t1.id as video_id, t1.cover_url as video_cover_url, t1.video_url, t1.video_duration,
                            t2.theatre_id, t2.episode, t2.intro as video_title
                        from hobby_star_blog.t_star_blog t1
                        join hobby_star_blog.t_theatre_episode t2 on t1.id=t2.star_blog_id
                        where t1.deleted=0 and t2.deleted=0 and t2.status=1
                        )""", config=config, mysql_config='1')
    print(video_info.head(10))

    # theatre_video_info = pd.merge(theatre_info, video_info, on='theatre_id')
    # print(theatre_video_info)
    #
    # theatre_video_info.to_csv('data/theatre_video_info.csv', index=False)



def func_main():

    """
    本程序主要是获取视频信息
    获取特征主要以单个视频为出发起点，因为有多重（单个、合计等）类型，但是最终都会落到单个视频

    先做单个视频推荐

    视频推荐主要因素：标题、封面、视频、各种描述、标签等等
    先获取这些基础信息，然后再做特征处理

    从短剧小视频为出发点
    """
    # func_get_theatre_video()

    # t_star_blog = get_data_from_mysql(sql_input="""(
    #                     select *
    #                     from hobby_star_blog.t_star_blog
    #                     where deleted=0
    #                     limit 1000
    #                 )""", config=config,mysql_config='1')
    # print(t_star_blog)
    #
    video_info = get_data_from_mysql(sql_input="""(
                        select t2.id as video_id, t2.drama_id, t2.episode_tags, t2.episode, t2.introduction,
                            t3.*
                        from hobby_star_blog.t_star_blog_drama_video_relation t2
                        join hobby_star_blog.t_star_blog t3 on t2.business_id = t3.id
                        where t2.deleted=0 and t3.deleted=0
                        )""", config=config, mysql_config='1')
    print(video_info)
    print(video_info.head(30)[['id', 'title', 'content_desc', 'cover_url', 'video_url', 'video_duration', 'release_source']].to_dict(orient='records'))


if __name__ == '__main__':
    """
    视频向量化
    文本：w2v, bert, dssm

    图片：
    """
    print("扛起大刀。。。")
    env_ = sys.argv[1]
    config = get_env_config(env_)
    print(config)
    func_main()


