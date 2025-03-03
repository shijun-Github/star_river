import os
import sys
from pprint import pprint

import pandas as pd
from sklearn.utils import shuffle

from rapidfuzz import process

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


def func_get_video_series_info_by_item_id(req, data):
    """
    剧集级别的， 单集级别
     随机从剧集池子中获取 batch_size个剧集
     """
    page_index, page_size = req['page_index'], req['page_size']
    video_info = data
    video_info['drama_id'] = video_info['drama_id'].astype(str)
    video_info = video_info[video_info['drama_id']==str(req['item_info']['drama_id'])]
    video_page = video_info[page_index * page_size:(page_index + 1) * page_size]
    video_page = video_page.sort_values(by=['episode'], ascending=True)
    # video_page = video_page.rename(columns={'video_id': 'id', 'drama_name': 'name', 'drama_desc': 'desc'})
    # 生成条件掩码 # 仅对符合条件的行操作
    mask = video_page['drama_type'].isin([0, 3])
    video_page.loc[mask, 'drama_name'] = "第" + video_page['episode'].astype(str) + "集|" + video_page['drama_name']
    print(video_page)
    return video_page


def func_search_drama_by_keyword(req_in, data):
    """
    剧集级别的， 单集级别
     随机从剧集池子中获取 batch_size个剧集
     """
    print('++++++++++++++++++++++++++++++++++++++')
    print(data)
    print(req_in)
    video_info = data[data['drama_type'].isin(req_in['video_type'])]
    print(video_info)
    print(video_info.groupby('drama_type').size())
    drama_id_list = video_info['drama_id'].tolist()
    drama_name_list = video_info['drama_name'].tolist()
    # print(drama_name_list)
    # 查找与目标字符串最匹配的多个字符串
    best_matches = process.extract(req_in['keyword'], drama_name_list, limit=req_in['page_size'])
    print(f"多个最佳匹配: {best_matches}")
    index_list = [item[2] for item in best_matches]
    ids = [drama_id_list[item] for item in index_list]
    # 筛选出 drama_id 列包含在 ids 列表中的行
    filtered_df = data[data['drama_id'].isin(ids)].copy()
    # 将 drama_id 列转换为 Categorical 类型，并指定顺序
    filtered_df['drama_id'] = pd.Categorical(filtered_df['drama_id'], categories=ids, ordered=True)
    # 按照 drama_id 列排序
    filtered_df = filtered_df.sort_values(by='drama_id')
    return filtered_df
if __name__ == '__main__':
    """ 
    这里是兜底数据，保证至少又内容可以推出来
     1、随机获取一部分剧
     2、获取热门的剧
    """
    # req = {
    #     'page_index': 0,
    #     'page_size': 4,
    #     'item_id': '1891346472892174337'
    # }


    # req = {'user_id': 'dkafa12e2j',
    #        'page_index': 0, 'page_size': 8,
    #        'item_info': {'drama_id': '1867011550933733378'}}
    # file_path = os.path.abspath(__file__).split('recall')[0] + 'data/video_info.csv'
    # video_info = pd.read_csv(file_path)
    # data_page = func_get_video_series_info_by_item_id(req, video_info)
    # t = data_page.to_dict(orient='records')
    # for item in t:
    #     pprint(item)
    # #     item['cover'] = item['drama_cover_url']
    # #     item['name'] = item['drama_name']
    # #     item['desc'] = item['drama_desc']
    # # pprint(t)

    req = {
        'page_index': 1,
        'page_size': 10,
        'keyword': '甄嬛传'
    }
    data_info = pd.read_csv(os.path.abspath(__file__).split('recall')[0] + 'data/drama_info.csv')
    data_page = func_search_drama_by_keyword(req, data_info)
    print(data_page)




