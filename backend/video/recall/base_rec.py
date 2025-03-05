import os
import sys
from pprint import pprint

import pandas as pd
from sklearn.utils import shuffle

# import pandas as pd
#
# from aa_recommend_complete_project.com_service import video_info
# from code_test import drama_info_tan
pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列

def func_random_get_drama(req, data):
    """
    剧级别的
     随机从剧池子中获取 batch_size个剧
     """
    page_index, page_size = req['page_index'], req['page_size']
    # drama_info = pd.read_csv(os.path.abspath(__file__).split('recall')[0] + 'data/video_info.csv')
    drama_info = data
    drama_info = drama_info[drama_info['drama_type'].isin(req['video_type'])]
    drama_info = shuffle(drama_info)
    drama_page = drama_info[page_index * page_size:(page_index + 1) * page_size]
    # drama_page = drama_page.rename(columns={'drama_id': 'id', 'drama_name': 'name', 'drama_desc': 'desc', 'drama_cover_url': 'cover_url'})
    # drama_page = drama_page[['id', 'name', 'cover_url', 'desc']]
    print(drama_page)
    return drama_page


def func_random_get_video(req, data):
    """
    剧集级别的， 单集级别
     随机从剧集池子中获取 batch_size个剧集
     """
    page_index, page_size = req['page_index'], req['page_size']
    # file_path = os.path.abspath(__file__).split('recall')[0] + 'data/video_info.csv'
    # video_info = pd.read_csv(file_path)
    video_info = data
    video_info = video_info[video_info['drama_type'].isin(req['video_type'])]
    video_info = video_info[video_info['video_url'].str.contains("prod")]
    # video_info['episode'] = video_info['episode'].astype(int)
    video_info = video_info[video_info['episode']==1]
    print(video_info)
    print(video_info.groupby('episode').size())
    print('+++++++++++++++++++++++++++++++++++++++++')
    video_info = shuffle(video_info)
    video_page = video_info[page_index * page_size:(page_index + 1) * page_size]
    print(video_page)
    video_page = video_page.rename(columns={'video_id': 'id', 'drama_name': 'name', 'drama_desc': 'desc'})
    # video_page = video_page[['id', 'name', 'cover_url', 'desc']]
    print(video_page)
    return video_page


if __name__ == '__main__':
    """ 
    这里是兜底数据，保证至少又内容可以推出来
     1、随机获取一部分剧
     2、获取热门的剧
     """

    req = {
        'page_index': 1,
        'page_size': 40,
        'video_type':[0]
    }
    file_path = os.path.abspath(__file__).split('recall')[0] + 'data/video_info.csv'
    video_info = pd.read_csv(file_path)
    data_page = func_random_get_video(req, video_info)
    t = data_page.to_dict(orient='records')
    for item in t:
        pprint(item)
    #     item['cover'] = item['drama_cover_url']
    #     item['name'] = item['drama_name']
    #     item['desc'] = item['drama_desc']
    # pprint(t)




