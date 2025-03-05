import json
import time
from pprint import pprint

import pandas as pd
from sklearn.utils import shuffle

from utils.func_mysql import get_data_from_mysql

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列
import sys
sys.path.append('../..')  # 假设'..'是drama和utils的父目录
# from utils.func_mysql import get_data_from_mysql
from utils.get_data_self import get_data_from_tablestore
from utils.config_constants import get_env_config


def hot_recall_click_rate(parm):
    """ 热门召回，热门的维度是点击率 """
    config = get_env_config('uat')
    # video_realtime_info = get_data_from_tablestore("""(
    #                                    select item_id, click_rate
    #                                    from ads_recommend_gameplay_features_event_date_d_inc_dt
    #                                    where source in (0) and length(theatre_id)>0
    #                                    # order by click_rate ASC
    #                                    limit 10000
    #                                    )""", config['env'],'1')
    # print(video_realtime_info)
    # short_dramas = short_dramas[~short_dramas['describe'].isin([None, ''])]
    # short_dramas = short_dramas.drop_duplicates(subset=['theatre_id'])

    video_info = get_data_from_mysql(sql_input="""(
                        select t1.id as video_id, t1.cover_url as video_cover_url, t1.video_url, t1.video_duration,
                            t2.id as item_id , t2.theatre_id, t2.episode, t2.intro as video_title
                        from hobby_star_blog.t_star_blog t1
                        join hobby_star_blog.t_theatre_episode t2 on t1.id=t2.star_blog_id
                        where t1.deleted=0 and t2.deleted=0 and t2.status=1 and episode=1
                        )""", config=config, mysql_config='1')
    video_info = video_info[['item_id', 'episode', 'video_url', 'video_title']]
    print(video_info)
    item_ids = video_info['item_id'].tolist()[:10000]
    item_ids = ','.join([str(item) for item in item_ids])

    # source in (0) and length(theatre_id)>0   获取的内容都是短剧
    video_info_realtime = get_data_from_tablestore("""(
                                    select *
                                    from app_recommend_gameplay_features_event_date_d_inc_dt
                                    where source in (0) and length(theatre_id)>0 
                                        and report_date = '2025-01-09' AND  item_id in (%s)
                                 )""" % item_ids, config['env'], '1')
    video_info_realtime['item_id'] = video_info_realtime['item_id'].astype(int)
    print(video_info_realtime)
    # print(video_info_realtime[['expose_num_1', 'click_num_1', 'duration_1', 'duration_rate', 'expose_num', 'click_num', 'duration', 'duration_rate']].sort_values(by='expose_num', ascending=False))

    res = pd.merge(video_info, video_info_realtime, on='item_id', how='inner')
    res = res.sort_values(by='duration_1', ascending=False)
    res = res.head(100)  # 该路召回数量为100
    return res


if __name__ == '__main__':
    """
    热门召回，各个维度的热门召回
    没有其他路召回可以兜底
    """
    parm_ = {
        'env': 'uat',
        'page_index': 1,
        'page_size': 10,
        'channel': '探剧'
    }

    hot_recall_click_rate(parm_)


