import os
import sys
from pprint import pprint

import pandas as pd
from sklearn.utils import shuffle
from rapidfuzz import process



def func_key_word_search_drama(req_in, data):
    """
    剧集级别的， 单集级别
     随机从剧集池子中获取 batch_size个剧集
     """
    drama_id_list = data['drama_id'].tolist()
    drama_name_list = data['drama_name'].tolist()
    # print(drama_name_list)
    # 查找与目标字符串最匹配的多个字符串
    best_matches = process.extract(req_in['keyword'], drama_name_list, limit=5)
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

    req = {
        'page_index': 1,
        'page_size': 10,
        'keyword': '甄嬛传'
    }
    data_info = pd.read_csv(os.path.abspath(__file__).split('recall')[0] + 'data/drama_info.csv')
    data_page = func_key_word_search_drama(req, data_info)
    print(data_page)
    # t = data_page.to_dict(orient='records')
    # for i in t:
    #     pprint(i)

